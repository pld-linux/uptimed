#
# TODO:
# - find other way to start than messing with rc.sysinit and rc.local
#	new one uses rc.script 
# - add CGI stuff
#
Summary:	Uptime record daemon - keeps track of the highest system uptimes
Summary(pl.UTF-8):	Demon śledzący największe uptime serwera
Name:		uptimed
Version:	0.3.12
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://podgorny.cz/uptimed/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	c523d6434b672107ea00559bb38eb050
URL:		http://podgorny.cz/moin/Uptimed
Patch0:		%{name}-DESTDIR.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Requires(post):	grep
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Uptimed is an uptime record daemon keeping track of the highest
uptimes the system ever had. Instead of using a pid-file to keep
sessions apart from eachother it uses the boottime from /proc/stat.
Uptimed comes with a console front-end to parse the records, which can
also easily be used to show your records on your Web page.

%description -l pl.UTF-8
Uptimed to demon zapisujący rekordy uptime, śledzący największe uptime
jakie miał system. Zamiast używać pliku pid do oddzielania sesji,
używa boottime z /proc/stat. Uptimed przychodzi z konsolowym
frontendem do parsowania rekordów, którego można łatwo użyć do
pokazywania rekordów na stronie WWW.

%prep
%setup -q
%patch0

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/uptimed.conf{-dist,}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q uptimed /etc/rc.d/rc.local ; then
	echo "echo \"Starting uptime daemon...\"" >> /etc/rc.d/rc.local
	echo "/usr/sbin/uptimed" >> /etc/rc.d/rc.local
fi
if ! grep -q uptimed /etc/rc.d/rc.sysinit ; then
	echo "echo \"Creating unique uptime daemon bootid...\"" >> /etc/rc.d/rc.sysinit
	echo "/usr/sbin/uptimed -b" >> /etc/rc.d/rc.sysinit
fi

%postun
echo "Please edit /etc/rc.d/rc.local and /etc/rc.d/rc.sysinit and take out the following lines"
echo "They should be at the very bottom of the file.."
echo ""
echo "-- /etc/rc.d/rc.local --"
echo "echo \"Starting uptime daemon...\""
echo "/usr/sbin/uptimed"
echo "-- /etc/rc.d/rc.sysinit --"
echo "echo \"Creating unique uptime daemon bootid...\""
echo "/usr/sbin/uptimed -b"

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog README* TODO
%attr(755,root,root) %{_sbindir}/uptimed
%attr(755,root,root) %{_bindir}/uprecords
%attr(755,root,root) %{_libdir}/*.so*
%{_libdir}/*a
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uptimed.conf
%{_mandir}/man*/*
%dir /var/spool/uptimed
