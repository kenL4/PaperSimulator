let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    pkgs.python312Full
    pkgs.python312Packages.numpy
    pkgs.python312Packages.matplotlib
    pkgs.python312Packages.pandas
    pkgs.python312Packages.pyvista

    # lsp
    pkgs.python312Packages.python-lsp-server
    pkgs.python312Packages.pylsp-rope
    pkgs.python312Packages.pyflakes
    pkgs.python312Packages.pycodestyle
  ];
}
