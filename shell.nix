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
        ipykernel
    ]
  )
).env

# nix-shell