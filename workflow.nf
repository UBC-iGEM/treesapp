params.bin = null

if (params.bin == null) {
    error "Missing required parameter (bin name): --bin"
}

bins = params.bin.split(',') as List

workflow {
    Channel
        .from(bins)
        .map { bin -> [bin, file("${bin}.msa.fasta")] }
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
