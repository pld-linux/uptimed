Name:		uptimed
Version:	0.1.5
Summary:	Is an uptime record daemon that keeps track of the highest uptimes the system has ever had.
Release:	1
License:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
URL:		http://capsi.cx/code-uptimed.html
Source0:	http://capsi.cx/src/uptimed/%{name}-%{version}.tar.bz2
Patch0:		uptimed-matt.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Uptimed is an uptime record daemon keeping track of the highest
uptimes the system ever had. Instead of using a pid-file to keep
sessions apart from eachother it uses the boottime from /proc/stat.
Uptimed comes with a console front-end to parse the records, which can
also easily be used to show your records on your Web page.

%prep
%setup -q
%patch0 -p1

%build
make linux

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}{%{_bindir},%{_sysconfdir}}

make install

gzip -9fn AUTHOR BUGS CREDITS ChangeLog TODO README*

%clean
rm -fr $RPM_BUILD_ROOT

%post
echo "echo \"Starting uptime daemon...\"" >> /etc/rc.d/rc.local
echo "/usr/local/bin/uptimed" >> /etc/rc.d/rc.local
echo "echo \"Creating unique uptime daemon bootid...\"" >> /etc/rc.d/rc.sysinit
echo "/usr/local/bin/uptimed -boot" >> /etc/rc.d/rc.sysinit

%postun
echo "Please edit /etc/rc.d/rc.local and /etc/rc.d/rc.sysinit and take out the following lines"
echo "They should be at the very bottom of the file.."
echo ""
echo "-- /etc/rc.d/rc.local --"
echo "echo \"Starting uptime daemon...\""
echo "/usr/local/bin/uptimed"
echo "-- /etc/rc.d/rc.sysinit --"
echo "echo \"Creating unique uptime daemon bootid...\""
echo "/usr/local/bin/uptimed -boot"

%files
%defattr(644,root,root,755)
%doc {AUTHOR,BUGS,CREDITS,ChangeLog,TODO}.gz
%doc README*.gz

%attr(755,root,root) %{_bindir}/uptimed
%attr(755,root,root) %{_bindir}/uprecords

%dir /var/spool/uptimed
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/uptimed.conf
