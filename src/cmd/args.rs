#![allow(warnings)]

use crate::errs;

pub fn parse_args(args: Vec<String>, paths: Vec<&str>) {

    let (flags, args) = filter_flags_from(args);
    let func = &args[0].to_owned();
    
    match func.as_str() {
        "list"      => println!("tmp"),
        "new"       => println!("tmp"),
        "remove"    => println!("tmp"),
        "search"    => println!("tmp"),
        "source"    => println!("tmp"),
        "update"    => println!("tmp"),
        _           => errs::unknown_cmd(&func)
    }

}

fn filter_flags_from(args: Vec<String>) -> (Vec<char>, Vec<String>) {
    
    let mut flags: Vec<char> = vec!();
    let mut _args: Vec<String> = vec!();

    for arg in args {
        if arg.contains("-") {
            let _flags: Vec<char> = arg.chars()
                                       .filter(|c| c != &'-')
                                       .collect();

            for c in _flags {
                flags.push(c);
            }

        } else {
            _args.push(arg);
        }
    }

    return (flags, _args);
}