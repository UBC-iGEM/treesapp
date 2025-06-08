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

process treesapp_ch {
    input:
    val bin_name

    output:
    path 'output' optional true

    script:
    """
    mkdir treesapp_${bin_name}
    cd treesapp_${bin_name}
    treesapp create --verbose --fast -c aCA${bin_name} -i ../${bin_name}.msa.fasta
    """
}
