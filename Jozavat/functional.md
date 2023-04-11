<div dir=rtl>
<h1>برنامه‌نویسی Functional</h1>
</div>

<div dir=rtl>
یه ماشینی هست به اسم ماشین تورینگ، این ماشین یه سری کارهای مهمی
رو انجام میده
<br>
ماشین تورینگ: به زبان‌های برنامه نویسی که می‌تونه کارهای
 ماشین تورینگ رو انجام بده، تورینگ کامپلیت می‌گن.
<br>
پس بنابراین اگه زبانی، تورینگ کامپلیت باشه، یعنی تمام کارهای
لازم برای یه برنامه‌نویس رو انجام میده
<br><br>
با ریاضی میشه اثبات کرد که یه زبان تورینگ کامپیلیت هست یا ن.
<br><br>
زبان‌های برنامه نویسی فانکشنال تورینگ کامپلیت هستن همشون چون باید قابلیت‌های لازم رو داشته باشن.
<br><br>
باید همه کار‌هایی رو که با کلاس میشه کرد با اون فانکشنال‌ها بشه کرد.
<br><br>
وقتی داخل یه زبان برنامه‌نویسی فانکشنال داریم یه تابع رو صدا می‌زنیم، دیتاها کجا ذخیره میشن؟
<br><br>
مثلا متراژ خونه رو باید داخل فانکشن ذخیره کرد.
<br><br>
کلی تکنیک هست که بعضی‌هاشو میشه تو زبان‌های غیر فانکشنال هم اجرا کرد.
<br><br>
فرض کنیم که نمیخوایم از این استفاده کنیم:
</div>

```py
def sum(a,b):
    return a+b
```

<div dir=rtl>
پس یعنی شبیه این:
</div>

```py
def sum10(a):
    return a+10

def sum15(a):
    return a+15
```

<div dir=rtl>
یه تکنیک هست که تو پایتون هم میشه استفاده کرد.
</div>

```py
def sum_maker(b):
    def f(a):
        return a+b
    return f
```

<div dir=rtl>
مثلا برای مثال املاکی اینجوری استفاده می‌شه:
</div>

```py
def amlak(x,y,z,...):
    def get_metrage():
        return x
    return get_metrage
```

<div dir=rtl>
بنابراین در یک برنامه functional خالص و pure مثل purely تنها همین خط اجرا می‌شه:
</div>

```py
a(b(c(d(f(e)))))
```

<div dir=rtl>
این روش برا برنامه‌های concurrent و برنامه‌های حساس خیلی خوبه چرا؟
چون دیتا هیچ وقت تغییر نمی‌کنه!
<br>
مثلا اگه بخوایم متراژ خونه رو عوض کنیم، باید یه کپی از خونه با اون متراژی که می‌خوایم بگیریم.
<br>
<br>
<h3>
یه سوال!
</h3>
<br>
یه کد مشخص رو چند نفر اجرا میکنن و به ترتیب هم نیست ولی دیتا‌ها شیر میشه و یه مقدار ثابتی رو هر متغیر و هر نفر می‌بینه
</div>

```py
a = 0
Lock = False
if Lock == False:
    a = 1
    Lock = True
else:
    return
```

<div dir=rtl>
چه کنیم که وقتی هر دو نفر همزمان این کد رو ران می‌کنن
یه نفر تغییر بده یه نفر تغییر نده؟
<br>
برنامه‌نویسی موازی!
</div>