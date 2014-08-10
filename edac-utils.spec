Summary:	Userspace helper for Linux kernel EDAC drivers (ECC)
Summary(pl.UTF-8):	Narzędzia pomocnicze sterownika EDAC (ECC)
Name:		edac-utils
Version:	0.16
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/edac-utils/%{name}-%{version}.tar.bz2
# Source0-md5:	77dda84f25ddba732da1d94fe357bf87
URL:		http://sourceforge.net/projects/edac-utils/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
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

%package devel
Summary:	Header files for edac library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki edac
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#%{_rm} $RPM_BUILD_ROOT%{_libdir}/libedac.la

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
%ghost %{_libdir}/libedac.so.0
%{_mandir}/man1/edac-util.1*
%{_mandir}/man8/edac-ctl.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libedac.so
%{_libdir}/libsysfs.la
%{_includedir}/edac.h
%{_mandir}/man3/edac.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libedac.a
