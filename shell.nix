{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.numpy
    pkgs.zlib
    pkgs.gcc
    pkgs.opencv
    pkgs.glib
    # Add other dependencies as needed
  ];
  shell = pkgs.mkShell { buildInputs = [ pkgs.zsh ]; };
  # shellHook = ''
  #   export LD_LIBRARY_PATH=$(for p in ${pkgs.zlib} ${pkgs.gcc} ${pkgs.opencv} ${pkgs.glib}; do echo -n "$p/lib:"; done)$LD_LIBRARY_PATH
  # '';
  shellHook = ''
    export LD_LIBRARY_PATH=$(for p in ${pkgs.zlib} ${pkgs.gcc} ${pkgs.opencv} ${pkgs.glib}; do echo -n "$p/lib:"; done)$LD_LIBRARY_PATH
  '';
}
