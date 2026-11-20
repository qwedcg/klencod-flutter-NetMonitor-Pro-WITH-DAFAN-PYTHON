package com.netmonitor.pro;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.net.VpnService;
import android.os.Build;
import android.os.IBinder;
import android.os.ParcelFileDescriptor;

import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Locale;

public class MonitorVpnService extends VpnService {
    public static volatile boolean running = false;

    private static final int NOTIFICATION_ID = 1001;
    private static final String CHANNEL_ID = "netmonitor";

    private ParcelFileDescriptor tun;
    private Thread worker;

    private final HashSet<String> ips = new HashSet<>();
    private final HashSet<Integer> ports = new HashSet<>();
    private long packets = 0;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (running) return START_STICKY;

        running = true;
        ArrayList<String> packages =
            intent == null ? null :
            intent.getStringArrayListExtra("apps");

        startForeground(NOTIFICATION_ID, buildNotification());
        startCapture(packages == null ? new ArrayList<>() : packages);

        return START_STICKY;
    }

    private Notification buildNotification() {
        NotificationManager nm =
            (NotificationManager)getSystemService(NOTIFICATION_SERVICE);

        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "NetMonitor Pro",
                NotificationManager.IMPORTANCE_LOW
            );
            nm.createNotificationChannel(channel);
        }

        Notification.Builder b = Build.VERSION.SDK_INT >= 26
            ? new Notification.Builder(this, CHANNEL_ID)
            : new Notification.Builder(this);

        return b.setContentTitle("NetMonitor Pro")
            .setContentText("مراقبة اتصالات التطبيقات تعمل")
            .setSmallIcon(android.R.drawable.stat_sys_upload)
            .setOngoing(true)
            .build();
    }

    private void startCapture(ArrayList<String> packages) {
        try {
            VpnService.Builder builder = new VpnService.Builder()
                .setSession("NetMonitor Pro")
                .setMtu(1500)
                .addAddress("10.10.0.2", 32)
                .addRoute("0.0.0.0", 0);

            /*
             * Only selected applications are routed through this VPN.
             * If nothing is selected, the service is stopped instead of
             * silently capturing the whole device.
             */
            if (packages.isEmpty()) {
                stopSelf();
                return;
            }

            for (String pkg : packages) {
                try {
                    builder.addAllowedApplication(pkg);
                } catch (Exception ignored) {
                }
            }

            tun = builder.establish();

            if (tun == null) {
                stopSelf();
                return;
            }

            worker = new Thread(this::readLoop, "NetMonitor-VPN");
            worker.start();

        } catch (Exception e) {
            stopSelf();
        }
    }

    private void readLoop() {
        byte[] buffer = new byte[32767];

        try (FileInputStream input =
                 new FileInputStream(tun.getFileDescriptor())) {

            while (running) {
                int length = input.read(buffer);
                if (length <= 0) continue;

                Packet packet = parseIpv4(buffer, length);
                if (packet == null) continue;

                packets++;
                ips.add(packet.remoteIp);
                ports.add(packet.remotePort);

                String line = String.format(
                    Locale.US,
                    "%s | %s | %d",
                    packet.protocol,
                    packet.remoteIp,
                    packet.remotePort
                );

                Intent result = new Intent("NETMONITOR_RESULT");
                result.setPackage(getPackageName());
                result.putExtra("line", line);
                sendBroadcast(result);

                Intent stat = new Intent("NETMONITOR_STATS");
                stat.setPackage(getPackageName());
                stat.putExtra("ips", ips.size());
                stat.putExtra("ports", ports.size());
                stat.putExtra("packets", packets);
                sendBroadcast(stat);
            }

        } catch (Exception ignored) {
        }
    }

    private static class Packet {
        final String protocol;
        final String remoteIp;
        final int remotePort;

        Packet(String protocol, String remoteIp, int remotePort) {
            this.protocol = protocol;
            this.remoteIp = remoteIp;
            this.remotePort = remotePort;
        }
    }

    /*
     * TUN gives raw IP packets.
     * For outbound traffic:
     *   destination = remote server
     *   destination port = remote port
     *
     * For inbound traffic:
     *   source = remote server
     *   source port = remote port
     *
     * We therefore use the VPN address to determine direction and always
     * display the remote endpoint.
     */
    private Packet parseIpv4(byte[] b, int len) {
        if (len < 20) return null;

        int version = (b[0] >>> 4) & 0x0F;
        if (version != 4) return null;

        int ihl = (b[0] & 0x0F) * 4;
        if (ihl < 20 || len < ihl + 4) return null;

        int protocol = b[9] & 0xFF;

        if (protocol != 6 && protocol != 17)
            return null;

        String src = ipv4(b, 12);
        String dst = ipv4(b, 16);

        int srcPort = u16(b, ihl);
        int dstPort = u16(b, ihl + 2);

        final String vpnIp = "10.10.0.2";

        String remoteIp;
        int remotePort;

        if (vpnIp.equals(dst)) {
            remoteIp = src;
            remotePort = srcPort;
        } else {
            remoteIp = dst;
            remotePort = dstPort;
        }

        if (remotePort <= 0 || remotePort > 65535)
            return null;

        return new Packet(
            protocol == 6 ? "TCP" : "UDP",
            remoteIp,
            remotePort
        );
    }

    private static int u16(byte[] b, int off) {
        return ((b[off] & 0xFF) << 8) | (b[off + 1] & 0xFF);
    }

    private static String ipv4(byte[] b, int off) {
        return (b[off] & 0xFF) + "." +
               (b[off + 1] & 0xFF) + "." +
               (b[off + 2] & 0xFF) + "." +
               (b[off + 3] & 0xFF);
    }

    @Override
    public void onDestroy() {
        running = false;

        if (worker != null) {
            try { worker.interrupt(); } catch (Exception ignored) {}
            worker = null;
        }

        if (tun != null) {
            try { tun.close(); } catch (Exception ignored) {}
            tun = null;
        }

        super.onDestroy();
    }

    @Override
    public void onRevoke() {
        stopSelf();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return super.onBind(intent);
    }
}
