params.bin = null
params.file = null

if (params.bin == null) {
    error "Missing required parameter (bin name): --bin"
}

if (params.file == null) {
    error "Missing required parameter (input filename): --file"
}

workflow {
    Channel
        .value([ params.bin, file(params.file) ])
        .set { bin_ch }

    treesapp(bin_ch)
}

process treesapp {
    input:
    tuple val(bin_name), path(msa_file)

    output:
    path 'output' optional true

    script:
    """
    export PATH="\$HOME/.pixi/bin:\$PATH"
    pixi run treesapp create --verbose --fast -c aCA${bin_name} -i ${msa_file}
    """
}
