package com.netmonitor.pro;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.net.VpnService;
import android.os.Build;
import android.os.Bundle;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.view.Window;
import android.widget.*;
import java.util.*;

public class MainActivity extends Activity {
    private static final int VPN_REQUEST = 501;

    private LinearLayout root;
    private TextView status, stats, results;
    private final ArrayList<String> selectedPackages = new ArrayList<>();
    private final ArrayList<AppItem> apps = new ArrayList<>();

    private final int BG = Color.rgb(8, 12, 20);
    private final int CARD = Color.rgb(18, 27, 42);
    private final int CYAN = Color.rgb(0, 220, 255);
    private final int GREEN = Color.rgb(0, 230, 140);
    private final int RED = Color.rgb(255, 75, 95);

    private static class AppItem {
        final String name, pkg;
        AppItem(String name, String pkg) {
            this.name = name;
            this.pkg = pkg;
        }
    }

    private final BroadcastReceiver receiver = new BroadcastReceiver() {
        @Override public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if ("NETMONITOR_RESULT".equals(action)) {
                addResult(intent.getStringExtra("line"));
            } else if ("NETMONITOR_STATS".equals(action)) {
                updateStats(
                    intent.getIntExtra("ips", 0),
                    intent.getIntExtra("ports", 0),
                    intent.getLongExtra("packets", 0)
                );
            }
        }
    };

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        buildUi();
        loadApps();

        IntentFilter filter = new IntentFilter();
        filter.addAction("NETMONITOR_RESULT");
        filter.addAction("NETMONITOR_STATS");

        if (Build.VERSION.SDK_INT >= 33) {
            registerReceiver(receiver, filter, Context.RECEIVER_NOT_EXPORTED);
        } else {
            registerReceiver(receiver, filter);
        }
    }

    @Override
    protected void onDestroy() {
        try { unregisterReceiver(receiver); } catch (Exception ignored) {}
        super.onDestroy();
    }

    private TextView text(String value, float size) {
        TextView t = new TextView(this);
        t.setText(value);
        t.setTextColor(Color.WHITE);
        t.setTextSize(size);
        t.setPadding(16, 12, 16, 12);
        return t;
    }

    private Button button(String value) {
        Button b = new Button(this);
        b.setText(value);
        b.setTextColor(Color.WHITE);
        b.setTextSize(15);
        b.setAllCaps(false);

        GradientDrawable bg = new GradientDrawable();
        bg.setColor(CARD);
        bg.setCornerRadius(24);
        bg.setStroke(2, CYAN);
        b.setBackground(bg);

        LinearLayout.LayoutParams p =
            new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT,
                                          LinearLayout.LayoutParams.WRAP_CONTENT);
        p.setMargins(8, 6, 8, 6);
        b.setLayoutParams(p);
        return b;
    }

    private void buildUi() {
        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(10, 10, 10, 10);
        root.setBackgroundColor(BG);

        TextView title = text("📡 NetMonitor Pro", 25);
        title.setTextColor(CYAN);
        root.addView(title);

        status = text("⏹ غير نشط", 16);
        status.setTextColor(RED);
        root.addView(status);

        stats = text("🌐 IPs: 0    🔌 Ports: 0    📦 Packets: 0", 15);
        root.addView(stats);

        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);

        Button monitor = button("🚀 بدء / إيقاف");
        Button choose = button("📱 اختيار التطبيقات");

        monitor.setOnClickListener(v -> toggleMonitor());
        choose.setOnClickListener(v -> showAppPicker());

        row.addView(monitor, new LinearLayout.LayoutParams(0,
                LinearLayout.LayoutParams.WRAP_CONTENT, 1));
        row.addView(choose, new LinearLayout.LayoutParams(0,
                LinearLayout.LayoutParams.WRAP_CONTENT, 1));
        root.addView(row);

        Button clear = button("🗑 مسح النتائج");
        clear.setOnClickListener(v -> {
            results.setText("لا توجد اتصالات بعد.");
            stats.setText("🌐 IPs: 0    🔌 Ports: 0    📦 Packets: 0");
        });
        root.addView(clear);

        results = text("لا توجد اتصالات بعد.\nاختر تطبيقًا ثم ابدأ المراقبة.", 14);
        ScrollView scroll = new ScrollView(this);
        scroll.addView(results);
        root.addView(scroll, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, 0, 1));

        setContentView(root);
    }

    private void loadApps() {
        PackageManager pm = getPackageManager();
        Intent launcher = new Intent(Intent.ACTION_MAIN);
        launcher.addCategory(Intent.CATEGORY_LAUNCHER);

        List<android.content.pm.ResolveInfo> list =
            pm.queryIntentActivities(launcher, PackageManager.MATCH_ALL);

        apps.clear();

        for (android.content.pm.ResolveInfo info : list) {
            ApplicationInfo ai = info.activityInfo.applicationInfo;
            if (getPackageName().equals(ai.packageName)) continue;

            String name = pm.getApplicationLabel(ai).toString();
            apps.add(new AppItem(name, ai.packageName));
        }

        Collections.sort(apps, (a, b) ->
            a.name.compareToIgnoreCase(b.name));
    }

    private void showAppPicker() {
        if (apps.isEmpty()) {
            toast("لم يتم العثور على تطبيقات قابلة للتشغيل");
            return;
        }

        LinearLayout rows = new LinearLayout(this);
        rows.setOrientation(LinearLayout.VERTICAL);

        for (AppItem app : apps) {
            CheckBox cb = new CheckBox(this);
            cb.setText(app.name + "\n" + app.pkg);
            cb.setTextColor(Color.WHITE);
            cb.setChecked(selectedPackages.contains(app.pkg));

            cb.setOnCheckedChangeListener((button, checked) -> {
                if (checked) {
                    if (!selectedPackages.contains(app.pkg))
                        selectedPackages.add(app.pkg);
                } else {
                    selectedPackages.remove(app.pkg);
                }
            });

            rows.addView(cb);
        }

        ScrollView scroll = new ScrollView(this);
        scroll.addView(rows);

        AlertDialog dialog = new AlertDialog.Builder(this)
            .setTitle("📱 اختر التطبيقات للمراقبة")
            .setView(scroll)
            .setPositiveButton("حفظ", null)
            .setNegativeButton("إلغاء", null)
            .create();

        dialog.show();

        Window window = dialog.getWindow();
        if (window != null) {
            int h = (int)(getResources().getDisplayMetrics().heightPixels * 0.75f);
            window.setLayout(-1, h);
        }
    }

    private void toggleMonitor() {
        if (MonitorVpnService.running) {
            stopMonitor();
            return;
        }

        if (selectedPackages.isEmpty()) {
            toast("اختر تطبيقًا واحدًا على الأقل");
            return;
        }

        Intent prepare = VpnService.prepare(this);
        if (prepare != null) {
            startActivityForResult(prepare, VPN_REQUEST);
        } else {
            startMonitor();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == VPN_REQUEST && resultCode == RESULT_OK) {
            startMonitor();
        }
    }

    private void startMonitor() {
        Intent intent = new Intent(this, MonitorVpnService.class);
        intent.putStringArrayListExtra("apps", selectedPackages);

        if (Build.VERSION.SDK_INT >= 26) {
            startForegroundService(intent);
        } else {
            startService(intent);
        }

        status.setText("🟢 جاري المراقبة...");
        status.setTextColor(GREEN);
    }

    private void stopMonitor() {
        stopService(new Intent(this, MonitorVpnService.class));
        status.setText("⛔ تم الإيقاف");
        status.setTextColor(RED);
    }

    private void addResult(String line) {
        if (line == null || line.isEmpty()) return;

        runOnUiThread(() -> {
            if (results.getText().toString().startsWith("لا توجد اتصالات"))
                results.setText("");

            results.append(line + "\n");
        });
    }

    private void updateStats(int ipCount, int portCount, long packetCount) {
        runOnUiThread(() -> stats.setText(
            "🌐 IPs: " + ipCount +
            "    🔌 Ports: " + portCount +
            "    📦 Packets: " + packetCount
        ));
    }

    private void toast(String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }
}
