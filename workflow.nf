params.bin = null

if (params.bin == null) {
    error "Missing required parameter (bin name): --bin"
}

workflow {
    Channel
        .value(params.bin)
        .map { bin ->  [bin, file("${bin}.msa.fasta")] }
        .set { treesapp_ch }
    treesapp(treesapp_ch)
}

process treesapp {
    input:
    val bin_name
    path msa_file

    output:
    path 'output' optional true

    script:
    """
    export PATH="\$HOME/.pixi/bin:\$PATH"
    pixi run treesapp create --verbose --fast -c aCA${bin_name} -i ${msa_file}
    """
}
