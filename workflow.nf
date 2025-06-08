params.bin = null

if (params.bin == null) {
    error "Missing required parameter (bin name): --bin"
}

workflow {
    Channel
        .value(params.bin)
        .set { treesapp_ch }
    treesapp(treesapp_ch)
}

process treesapp {
    input:
    val bin_name

    output:
    path 'output' optional true

    script:
    """
    export PATH="\$HOME/.pixi/bin:\$PATH"
    mkdir treesapp_${bin_name}
    cd treesapp_${bin_name}
    pixi run treesapp create --verbose --fast -c aCA${bin_name} -i ../${bin_name}.msa.fasta
    """
}
