#![allow(warnings)]

mod colors;
mod cmd;
mod errs;
mod prints;

const DEF_CONF_DIR_PATH: &'static str = ".|user|/tumbo";
const DEF_SHELL_SOURCE_PATH: &'static str = ".bash_aliases";

fn main() {
    
    let args: Vec<String> = std::env::args().skip(1).collect();

    if args.len() == 0 {
        println!("{}", prints::draw_tumbo_no_args());
        
    } else {
        let paths = vec!(DEF_CONF_DIR_PATH, DEF_SHELL_SOURCE_PATH);
        cmd::args::parse_args(args, paths);
    }
}
