%define _empty_manifest_terminate_build 0
%global __python %{__python3}

Name: kitty
Summary: Fast, featureful, GPU based terminal emulator
Version:	0.47.2
Release:	1
Group: Terminals
License: GPL-3.0-only
URL: https://github.com/kovidgoyal/kitty
Source0: https://github.com/kovidgoyal/kitty/releases/download/v%{version}/kitty-%{version}.tar.xz
Source1:  https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/NerdFontsSymbolsOnly.tar.xz
### Go vendor source for kitty
# from within the source tree run the following:
# go mod vendor
# compress the resulting vendor directory and name according to the source seen below
# tar -cJvf kitty-0.47.2-vendor.tar.xz vendor
# place the vendored archive alongside the original source archive.
Source2:  %{name}-%{version}-vendor.tar.xz

BuildRequires:  git
BuildRequires:  pkgconfig(python)
BuildRequires:  python%{pyver}dist(sphinx)
BuildRequires:  python%{pyver}dist(sphinx-copybutton)
BuildRequires:  python%{pyver}dist(sphinx-inline-tabs)
BuildRequires:  pkgconfig(ImageMagick)
BuildRequires:  %{_lib}rsync-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  golang
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(openssl)
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
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(simde)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(cairo-fc)

Requires:	%{name}-shell-integration
Requires:	%{name}-terminfo
Recommends:	%{name}-doc

%description
Kitty supports modern terminal features like: graphics, unicode,
true-color, OpenType ligatures, mouse protocol, focus tracking, and
bracketed paste.
Kitty has a framework for "kittens", small terminal programs that can be used
to extend its functionality.

%package        terminfo
Summary:        The terminfo file for Kitty Terminal
License:        GPL-3.0-only

%description    terminfo
%{summary}.

%package        shell-integration
Summary:        Shell integration scripts for %{name}
License:        GPL-3.0-only AND MIT

%description    shell-integration
%{summary}.

%package        doc
Summary:        Documentation for %{name}
License:        GPL-3.0-only AND MIT
BuildArch:      noarch

%description    doc
%{summary}.


%prep
%autosetup -p1
mkdir fonts
tar -xf %{S:1} -C fonts
tar -xf %{S:2}

%build
export CC=%{__cc}

sed -i 's!-pedantic-errors -Werror!!g' setup.py
%__python3 setup.py linux-package --debug \
	--libdir-name %{_lib} \
	--update-check-interval=0

%install
install -d %{buildroot}/usr
cp -a linux-package/* %{buildroot}/usr

%{buildroot}%{_bindir}/kitten __complete__ setup bash | \
    install -Dm644 /dev/stdin %{buildroot}%{_datadir}/bash-completion/completions/%{name}

%{buildroot}%{_bindir}/kitten __complete__ setup zsh | \
    install -Dm644 /dev/stdin  %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

%{buildroot}%{_bindir}/kitten __complete__ setup fish | \
    install -Dm644 /dev/stdin %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

%{buildroot}%{_bindir}/kitty \
    +runpy 'from kitty.config import *; print(commented_out_default_config())' \
    | install -Dm644 /dev/stdin %{buildroot}%{_datadir}/%{name}/%{name}.conf.default

%files
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/kitten
%{_libdir}/%{name}
%exclude %{_libdir}/%{name}/shell-integration
%exclude %{_libdir}/%{name}/terminfo
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-open.desktop
%{_datadir}/icons/hicolor/*/*/*.{png,svg}
%{_mandir}/man{1,5}/*.{1,5}*

%files terminfo
%license LICENSE
%{_datadir}/terminfo/x/xterm-%{name}
%{_libdir}/%{name}/terminfo

%files shell-integration
%license LICENSE
%{_libdir}/%{name}/shell-integration
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/%{name}/%{name}.conf.default
%{_datadir}/zsh/site-functions/_%{name}

%files doc
%license LICENSE
%doc *.md *.rst *.asciidoc
%{_docdir}/%{name}/html/
%dir %{_docdir}/%{name}
