# GlaDOS-Auto-Checkin
用于GlaDOS机场的签到领取天数。

配合windows的计划任务来实现每天自动签到。

GLaDOS登录方式有两种，一种是通过邮件验证码，另一种是通过手机号验证码。这里只实现了邮件验证码的方式，并且没有实现自动获取邮件内验证码。当第一次登录或者登录失效后需要手动在控制台输入邮件里的验证码。

只需要在`config.ini`文件中配置email就可以使用