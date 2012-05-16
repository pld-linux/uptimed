#
# TODO:
# - add CGI stuff
#
Summary:	Uptime record daemon - keeps track of the highest system uptimes
Summary(pl.UTF-8):	Demon śledzący największe uptime serwera
Name:		uptimed
Version:	0.3.17
Release:	0.5
License:	GPL v2+
Group:		Applications/System
Source0:	http://podgorny.cz/uptimed/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	d342918ea3a5117c127c67c9d3ed74e6
Source1:	%{name}.init
URL:		http://podgorny.cz/moin/Uptimed
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Requires(post):	grep
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Temporary fix. unresolved symbol u_current
%define         skip_post_check_so      libuptimed\.so\.0\.0\.0

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
prezentacji rekordów na stronie WWW.

%prep
%setup -q
# remove bundled getopt
# it should be probably added as patch
%{__rm} -rf src/getopt.[ch]
%{__sed} --in-place -e 's/AC_REPLACE_FUNCS(getopt)//' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static 

%{__make} 

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# We don't need libuptimed.la libuptimed.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libuptimed.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libuptimed.so
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/uptimed.conf{-dist,}

# Create dir for init.d
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog README* TODO
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/uptimed
%attr(755,root,root) %{_bindir}/uprecords
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.0
#%{_libdir}/*a
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uptimed.conf
%{_mandir}/man*/*
%dir /var/spool/uptimed
