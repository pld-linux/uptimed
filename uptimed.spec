Summary:	Uptime record daemon that keeps track of the highest uptimes the system has ever had
Name:		uptimed
Version:	0.1.6
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://capsi.cx/src/uptimed/%{name}-%{version}.tar.bz2
URL:		http://capsi.cx/code-uptimed.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Uptimed is an uptime record daemon keeping track of the highest
uptimes the system ever had. Instead of using a pid-file to keep
sessions apart from eachother it uses the boottime from /proc/stat.
Uptimed comes with a console front-end to parse the records, which can
also easily be used to show your records on your Web page.

%prep
%setup -q

%build
%{__make} linux

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}{%{_bindir},%{_sbindir},%{_sysconfdir},%{_mandir}/man{1,8},/var/spool/uptimed}

install uptimed.conf ${RPM_BUILD_ROOT}%{_sysconfdir}
install uptimed ${RPM_BUILD_ROOT}%{_sbindir}
install uprecords ${RPM_BUILD_ROOT}%{_bindir}
install uptimed.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
install uprecords.1 ${RPM_BUILD_ROOT}%{_mandir}/man1

gzip -9nf AUTHOR BUGS CREDITS ChangeLog TODO README*

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "echo \"Starting uptime daemon...\"" >> /etc/rc.d/rc.local
echo "/usr/sbin/uptimed" >> /etc/rc.d/rc.local
echo "echo \"Creating unique uptime daemon bootid...\"" >> /etc/rc.d/rc.sysinit
echo "/usr/sbin/uptimed -boot" >> /etc/rc.d/rc.sysinit

%postun
echo "Please edit /etc/rc.d/rc.local and /etc/rc.d/rc.sysinit and take out the following lines"
echo "They should be at the very bottom of the file.."
echo ""
echo "-- /etc/rc.d/rc.local --"
echo "echo \"Starting uptime daemon...\""
echo "/usr/sbin/uptimed"
echo "-- /etc/rc.d/rc.sysinit --"
echo "echo \"Creating unique uptime daemon bootid...\""
echo "/usr/sbin/uptimed -boot"

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/uptimed
%attr(755,root,root) %{_bindir}/uprecords
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/uptimed.conf
%{_mandir}/man*/*
%dir /var/spool/uptimed
