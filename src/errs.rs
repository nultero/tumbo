use crate::colors;
use std::process;

fn ex() {
    process::exit(1);
}

pub fn unknown_cmd(arg: &str) {
    let err = format!("{}`{}` is not a valid command", colors::red_err(), colors::emph(arg));
    println!("{}", err);
    ex();
}