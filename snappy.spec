#
# Conditional build:
%bcond_without	tests		# unit tests
%bcond_without	static_libs	# static library

Summary:	Snappy - fast compression/decompression library
Summary(pl.UTF-8):	Snappy - biblioteka do szybkiej kompresji i dekompresji
Name:		snappy
Version:	1.2.2
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/snappy/releases
Source0:	https://github.com/google/snappy/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	30286dd6311dee1d5498c57f62eda7b8
Source1:	%{name}.pc.in
Patch0:		%{name}-gtest.patch
URL:		http://google.github.io/snappy/
BuildRequires:	cmake >= 3.10
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with tests}
BuildRequires:	gtest-devel
BuildRequires:	lzo-devel >= 2
BuildRequires:	zlib-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Snappy is a compression/decompression library. It does not aim for
maximum compression, or compatibility with any other compression
library; instead, it aims for very high speeds and reasonable
compression. For instance, compared to the fastest mode of zlib,
Snappy is an order of magnitude faster for most inputs, but the
resulting compressed files are anywhere from 20% to 100% bigger.

Snappy has the following properties:
- Fast: Compression speeds at 250 MB/sec and beyond, with no
  assembler code.
- Stable: Over the last few years, Snappy has compressed and
  decompressed petabytes of data in Google's production environment.
  The Snappy bitstream format is stable and will not change between
  versions.
- Robust: The Snappy decompressor is designed not to crash in the face
  of corrupted or malicious input.
- Free and open source software: Snappy is licensed under the Apache
  license, version 2.0.

Snappy has previously been called "Zippy" in some Google presentations
and the like.

%description -l pl.UTF-8
Snappy to biblioteka kompresująca i dekompresująca. Jej celem nie jest
maksymalna kompresja ani kompatybilność z żadną istniejącą biblioteką;
celem natomiast jest bardzo duża szybkość przy rozsądnej kompresji. Na
przykład, w porównaniu do najszybszego trybu zliba, Snappy jest rząd
wielkości szybszy dla większości danych, ale pliki wynikowe są większe
o 20 do 100%.

Biblioteka Snappy ma następujące cechy:
- jest szybka: potrafi przetwarzać 250 MB/s bez kodu w asemblerze
- jest stabilna: przez ostatnie kilka lat była używana do kompresji i
  dekompresji petabajtów danych w środowisku produkcyjnym Google'a;
  format strumienia Snappy jest stabilny i nie zmieni się między
  wersjami
- jest trwała: dekompresor Snappy został tak zaprojektowany, aby nie
  wykładać się na uszkodzonych lub błędnych danych wejściowych
- jest oprogramowaniem wolnodostępnym i z otwartymi źródłami, na
  licencji Apache w wersji 2.0.

Snappy wcześniej (np. na różnych prezentacjach Google'a) był nazywany
"Zippy".

%package devel
Summary:	Header files for Snappy library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Snappy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for Snappy library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Snappy.

%package static
Summary:	Static Snappy library
Summary(pl.UTF-8):	Statyczna biblioteka Snappy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Snappy library.

%description static -l pl.UTF-8
Statyczna biblioteka Snappy.

%prep
%setup -q
%patch -P0 -p1

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_CXX_STANDARD=17 \
	-DSNAPPY_BUILD_BENCHMARKS=OFF \
	%{!?with_tests:-DSNAPPY_BUILD_TESTS=OFF}

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	-DCMAKE_CXX_STANDARD=17 \
	-DSNAPPY_BUILD_BENCHMARKS=OFF \
	%{!?with_tests:-DSNAPPY_BUILD_TESTS=OFF}

%{__make}

%{?with_tests:ctest}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
# static first so that packaged cmake config files refer to shared library
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# ugh, they removed autotools support together with .pc file :/
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
sed -e 's,@prefix@,%{_prefix},g;s,@libdir@,%{_libdir},g;s,@version@,%{version},g' \
	%{SOURCE1} > $RPM_BUILD_ROOT%{_pkgconfigdir}/snappy.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md
%attr(755,root,root) %{_libdir}/libsnappy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsnappy.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsnappy.so
%{_includedir}/snappy*.h
%{_pkgconfigdir}/snappy.pc
%{_libdir}/cmake/Snappy

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsnappy.a
%endif
