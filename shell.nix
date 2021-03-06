# with import <nixpkgs> {};
with import <unstable> {
  config.allowUnfree = true;
};

(
  python36.withPackages (
    ps: with ps; [
        numpy
        toolz
        jupyter
        matplotlib
        scikitlearn
        pandas
        seaborn
        Keras
        tensorflowWithCuda
        cudnn_cudatoolkit_10
        ipykernel
    ]
  )
).env

# nix-shell