{ pkgs ? import <nixpkgs> { } }:
# let
#   python = let
#     packageOverrides = self: super: {
#       opencv3 = super.opencv3.override {
#         enableGtk2 = true;
#         gtk2 = pkgs.gtk2;
#         #enableFfmpeg = true; #here is how to add ffmpeg and other compilation flags
#         #ffmpeg_3 = pkgs.ffmpeg-full;
#       };
#     };
#   in pkgs.python3.override {
#     inherit packageOverrides;
#     self = python;
#   };
pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    # (python.withPackages (ps: with ps; [ opencv3 ]))
    pkgs.python312Packages.opencv-python
    pkgs.zlib
    pkgs.gcc
    pkgs.glib
    pkgs.gtk2
    pkgs.mesa
    pkgs.uv
    pkgs.openssl_3_3
  ];

  shell = pkgs.mkShell { buildInputs = [ pkgs.zsh ]; };

  shellHook = ''
    export LD_LIBRARY_PATH=$(for p in ${pkgs.openssl_3_3} ${pkgs.zlib} ${pkgs.mesa} ${pkgs.gcc} ${pkgs.opencv4} ${pkgs.glib} ${pkgs.stdenv.cc.cc.lib}; do echo -n "$p/lib:"; done)$LD_LIBRARY_PATH
    source ./.venv/bin/activate
  '';
}
