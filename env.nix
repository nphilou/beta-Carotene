with import <unstable> {};

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

# $ nix-build env.nix -o env
