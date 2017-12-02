#!/usr/bin/perl -w

use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);

print "Content-type: text/html\n\n";

# check authentication
if (open (IN,"/usr/syno/synoman/webman/modules/authenticate.cgi|")) {
    $user=<IN>;
    chop($user);
    close(IN);
}

# verify $user is in group administrators
$isadmin=false;
($name, $passwd, $gid, $members) = getgrnam('administrators');
for ($members) {
    if ("$_" == $user) {
        $isadmin="true"
    }
}

if ($isadmin ne "true") {
    print "<HTML><HEAD><TITLE>需要权限验证</TITLE></HEAD><BODY>请先使用管理员账号登陆，然后再来配置本套件<br/><br/></BODY></HTML>\n";
    die;
}

# default values
$tmplhtml{'saved'}="";
$tmplhtml{'USERNAME'}="";
$tmplhtml{'SHAREPATH'}="/volume4/Downloads";

# shall we save?
$action=param ('action');
if ($action eq "save") {
    if (open (OUT, ">/var/packages/easyexplorer/target/config")) {
    $username=param ('username');
    $sharepath=param ('sharepath');
    print OUT "USERNAME=$username\n";
    print OUT "SHAREPATH=$sharepath\n";
	close (OUT);
	$tmplhtml{'saved'}=" <small style=\"color:green;\">(保存成功)</small>";
    } else {
	$tmplhtml{'saved'}=" <small style=\"color:red;\">(出错了，无法保存配置)</small>";
    }
}

# shall we reset the led?
if ($action eq "resetled") {
    if (open (OUT, ">/dev/ttyS1")) {
	print OUT "8";
	close (OUT);
    }
}

# (re-)read the configuration
if (open (IN, "/var/packages/easyexplorer/target/config")) {
    while (<IN>) {
	chomp;
	s/#.//;
	s/^\s+//;
	s/\s+$//;
	my ($var, $value) = split(/\s*=\s*/, $_, 2);
	$tmplhtml{$var}=$value;
    }
    close (IN);
} else {
    $tmplhtml{'saved'}=" <small style=\"color:red;\">(无法读取配置)</small>";
}

# clear the log file?
if ($action eq "clearlog") {
    if (open (OUT, ">/var/packages/easyexplorer/target/bin/easy-explorer.log")) {
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$year += 1900; ## $year contains no. of years since 1900, to add 1900 to make Y2K compliant
	$dt = sprintf ("%04s-%02s-%02s %02s:%02s:%02s", $year, $mon, $mday, $hour, $min, $sec);
	print OUT "$dt: 日志文件清空<br/>\n";
	close (OUT);
    }
    $action = "log"
}

# shall we display the log?
if ($action eq "log") {
    if (open (IN, "log.html")) {
	while (<IN>) {
	    s/==:([^:]+):==/$tmplhtml{$1}/g;
	    print $_;
	}
	close (IN);
	if (open (IN, "/var/packages/easyexplorer/target/bin/easy-explorer.log")) {
	    while (<IN>) {
		print $_;
	    }
	    close (IN);
	}
	print "</code>\n</p>\n</body>\n</html>";
    }
} else {
    # print html page
    if (open (IN, "index.htmlt")) {
	while (<IN>) {
	    s/==:([^:]+):==/$tmplhtml{$1}/g;
	    print $_;
	}
	close (IN);
    }
}
