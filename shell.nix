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
        cudnn_cudatoolkit_10
        ipykernel
    ]
  )
).env

# nix-shell