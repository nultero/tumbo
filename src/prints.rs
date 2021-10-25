#![allow(warnings)]

pub fn draw_tumbo() -> String {
    return "
       /^__^\\
      / .  . \\
     /        \\
    /  \\/  \\/  \\
    \\__________/".to_owned();
}

pub fn draw_tumbo_hat() -> String {
    return "
        _____
       |     |
    ___|_____|___
      / .  . \\
     /        \\
    /  \\/  \\/  \\
    \\__________/".to_owned();
}

pub fn draw_tumbo_no_args() -> String {
    return "    
       /^__^\\     
      / .  . \\
     /        \\\u{261E}  no args given to Tumbo
    /  \\/      \\
    \\__________/\n".to_owned();
}
