with import <nixpkgs> {};

python36.withPackages (
  ps: with ps; [
    numpy
    toolz
    jupyter
    matplotlib
    scikitlearn
  ]
)
