Summary:	Snappy - fast compression/decompression library
Summary(pl.UTF-8):	Snappy - biblioteka do szybkiej kompresji i dekompresji
Name:		snappy
Version:	1.0.4
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: http://code.google.com/p/snappy/downloads/list
Source0:	http://snappy.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	b69151652e82168bc5c643bcd6f07162
URL:		http://code.google.com/p/snappy/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	pkgconfig
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

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# already as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/snappy

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libsnappy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsnappy.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsnappy.so
%{_libdir}/libsnappy.la
%{_includedir}/snappy*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libsnappy.a
