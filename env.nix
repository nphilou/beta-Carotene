with import <unstable> {
  config.allowUnfree = true;
};


# let python = pkgs.python36.override {
#   packageOverrides = self: super: {
#     pyzmq = super.pyzmq.overridePythonAttrs(old: rec {
#       pname = "pyzmq";
#       version = "18.0.1";
#       src = super.fetchPypi {
#         inherit pname version;
#         sha256 = "8b319805f6f7c907b101c864c3ca6cefc9db8ce0791356f180b1b644c7347e4c";
#       };
#     });
#   };
# };

# in python.withPackages (

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
  ]
)

# $ nix-build env.nix -o env
