use maestro::prelude::*;

#[maestro::main]
fn main() {
    let mode = arg!("mode");
    let result = match mode.as_str() {
        "cluster" => cluster(),
        "ungap" => ungap(),
        "extract" => extract_msa(),
        _ => panic!("mode must be one of cluster, ungap, or extract"),
    };
    println!("Process completed with result {result:#?}")
}

fn cluster() -> WorkflowResult {
    let input = arg!("cluster_input");
    process! {
        /// Clustering workflow
        name = format!("cluster_{input}"),
        executor = "default",
        inputs = [input],
        script = r#"
            cd-hit -i "$input" -o "$input"-filtered.fasta -c 0.5 -n 2
        "#
    }
}

fn ungap() -> WorkflowResult {
    let input = Path::new(arg!("ungap"));
    let stub = input
        .file_stem()
        .expect("ungap file should have a file stem")
        .to_string_lossy();
    process! {
        /// Ungap workflow
        name = format!("ungap_{stub}"),
        executor = "default",
        inputs = [input],
        args = [stub],
        script = r#"
            seqmagick convert "$input" "$stub".fasta --ungap --prune-empty
        "#
    }
}

fn extract_msa() -> WorkflowResult {
    let og = arg!("og");
    let db = arg!("db");

    process! {
        /// MSA extraction workflow
        name = format!("msa_extract_{og}"),
        executor = "default",
        inputs = [db],
        args = [og],
        script = r#"
            rg -P "^$og\t" "$db" \
              | cut -f4 \
              | base64 -d \
              | gunzip -c \
              > "$og".msa.fasta
        "#
    }
}
