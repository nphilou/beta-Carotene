with import <nixpkgs> {};

(
  python36.withPackages (
    ps: with ps; [
        numpy
        toolz
        jupyter
        matplotlib
        scikitlearn
        pandas
        Keras
        tensorflowWithCuda
        cudnn
    ]
  )
).env

# nix-shell