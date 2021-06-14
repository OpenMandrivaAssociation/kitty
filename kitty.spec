#global debug_package %{nil}
%global __python %{__python3}

Name: kitty
Summary: Fast, featureful, GPU based terminal emulator
Version:	0.21.1
Release:	1
Group: System/X11
License: GPLv3
URL: https://github.com/kovidgoyal/kitty
Source0: https://github.com/kovidgoyal/kitty/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  python-devel
BuildRequires:  python-sphinx
BuildRequires:  imagemagick-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(libpng)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libcanberra)

%description
Kitty supports modern terminal features like: graphics, unicode,
true-color, OpenType ligatures, mouse protocol, focus tracking, and
bracketed paste.

Kitty has a framework for "kittens", small terminal programs that can be used
to extend its functionality.

%package doc
Summary:        Documentation for the kitty terminal emulator
License:        GPLv3

%description doc
Documentation for the kitty terminal emulator

%prep
%setup -q

%build
export CC=%{__cc}
%{__python3} setup.py linux-package --debug --libdir-name %{_lib}

%install
install -d %{buildroot}/usr
cp -a linux-package/* %{buildroot}/usr

%files
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/terminfo/x/xterm-kitty
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man5/kitty.conf.5.*

%files doc
%doc LICENSE *.md *.rst *.asciidoc
%{_docdir}/kitty/html
