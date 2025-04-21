schtasks /Create ^
/TN "FishingYFP_Daily" ^
/TR "wscript.exe \"C:\home\python\yfp\fishing-piers-fan\scripts\run_yfp.vbs\"" ^
/SC DAILY ^
/ST 06:00 ^
/RL HIGHEST ^
/F
