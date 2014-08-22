# TODO: PLDify init script
%include	/usr/lib/rpm/macros.perl
Summary:	Userspace helper for Linux kernel EDAC drivers (ECC)
Summary(pl.UTF-8):	Narzędzia pomocnicze sterownika EDAC (ECC)
Name:		edac-utils
Version:	0.16
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/edac-utils/%{name}-%{version}.tar.bz2
# Source0-md5:	77dda84f25ddba732da1d94fe357bf87
URL:		http://sourceforge.net/projects/edac-utils/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpm-perlprov
BuildRequires:	sysfsutils-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
EDAC is the current set of drivers in the Linux kernel that handle
detection of ECC errors from memory controllers for most chipsets
on i386 and x86_64 architectures. This userspace component consists
an init script which loads EDAC DIMM labels at system boot, and can
optionally be configured to load a specific EDAC driver if this is
not done automatically at system startup. The package also includes a
library and utility for reporting current error counts from the EDAC
sysfs files.

%description -l pl.UTF-8
EDAC to aktualny zbiór sterowników w jądrze Linuksa, obsługujący
wykrywanie błędów ECC z kontrolerów pamięci dla większości układów
architektur i386 oraz x86_64. Niniejszy pakiet przestrzeni użytkownika
składa się ze skryptu init ładującego etykiety DIMM-ów EDAC przy
starcie systemu i mogącego opcjonalnie (w przypadku skonfigurowania)
wczytać określony sterownik EDAC, jeśli nie zostało to zrobione
automatycznie przy rozruchu. Pakiet zawiera także bibliotekę i
narzędzie do raportowania bieżących liczników błędów z plików sysfs
EDAC.

%package devel
Summary:	Header files for edac library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki edac
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	sysfsutils-devel

%description devel
Header files for edac library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki edac.

%package static
Summary:	Static edac library
Summary(pl.UTF-8):	Statyczna biblioteka edac
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static edac library.

%description static -l pl.UTF-8
Statyczna biblioteka edac.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/edac/labels.d,/etc/rc.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/init.d $RPM_BUILD_ROOT/etc/rc.d

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog DISCLAIMER NEWS README TODO
%attr(755,root,root) %{_bindir}/edac-util
%attr(755,root,root) %{_sbindir}/edac-ctl
%attr(755,root,root) %{_libdir}/libedac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libedac.so.0
%dir %{_sysconfdir}/edac
%dir %{_sysconfdir}/edac/labels.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/edac/labels.db
#%attr(754,root,root) /etc/rc.d/init.d/edac
%{_mandir}/man1/edac-util.1*
%{_mandir}/man8/edac-ctl.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libedac.so
%{_libdir}/libedac.la
%{_includedir}/edac.h
%{_mandir}/man3/edac.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libedac.a
