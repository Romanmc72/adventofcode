mod common;

/// Description
/// -----------
/// The main program for day 6.
fn main() {
    let (line, part) = common::get_file_and_part();
    let mut times: Vec<u64> = vec![];
    let mut distances: Vec<u64> = vec![];
    if part == 1 {
        times = common::split_text_to_numbers(
            line.get(0).unwrap().split(":").collect::<Vec<&str>>().get(1).unwrap()
        );
        distances = common::split_text_to_numbers(
            line.get(1).unwrap().split(":").collect::<Vec<&str>>().get(1).unwrap()
        );
    } else if part == 2 {
        times = common::split_text_to_numbers(
            line.get(0).unwrap().replace(" ", "").split(":").collect::<Vec<&str>>().get(1).unwrap()
        );
        distances = common::split_text_to_numbers(
            line.get(1).unwrap().replace(" ", "").split(":").collect::<Vec<&str>>().get(1).unwrap()
        );
    } else {
        panic!("Part 1 or 2 dude, pick one.");
    }
        let mut factor = 1;
        for index in 0..times.len() {
            let time = times.get(index).unwrap();
            let distance = distances.get(index).unwrap();
            let answer = options(time, distance);
            println!("{}", answer);
            factor *= answer;
        }
        println!("Times     = {:?}", times);
        println!("Distances = {:?}", distances);
        println!("Part {}   = {}", part, factor);
}


/// Description
/// -----------
/// Returns the number of options available to hold to start given a
/// particular chosen time and distance.
///
/// Params
/// ------
/// :time: u64
/// The time alloted for a given race.
///
/// :distance: u64
/// The best distance achieved for that time.
///
/// Return
/// ------
/// u64
/// The number of options for how long to hold the start for.
fn options(time: &u64, distance: &u64) -> u64 {
    println!("{} = ({} * x) - x**2", distance, time);
    // distance = (time - x) * x;
    // distance = time * x - x.pow(2);
    // 0 = -x.pow(2) + time * x - distance;
    // 0 = (x - time) * (-x + time); // where time * time = distance at the zero case
    // max will always be at time / 2
    // where > some number though...
    // 12 and 18 for 216... so at time where == 216, then it is all the +/- from the peak from there...
    // 9 = (7 - x) * x;
    // 9 = 7*x - x.pow(2);
    // 0 = -x.pow(2) + 7*x - 9;
    // 0 = (x + ) * (-x + )
    // -b +/- (b**2 - 4ac)**(0.5)
    // --------------------------
    //           2a
    let a = -1.0;
    let b = *time as f64;
    let c = -1.0 * *distance as f64;
    let sqrt_b_squared_minus_4ac = f64::sqrt(b.powf(2.0) - 4.0 * a * c);
    let negative_b = -1.0 * b;
    let min_number = (negative_b + sqrt_b_squared_minus_4ac) / (2.0 * a);
    let max_number = (negative_b - sqrt_b_squared_minus_4ac) / (2.0 * a);
    let mut lower = min_number.ceil() as u64;
    if min_number == lower as f64 {
        lower += 1;
    }
    let mut upper = max_number.floor() as u64;
    if max_number == upper as f64 {
        upper -= 1;
    }
    if lower > upper {
        panic!("Looks like something went wrong! the lower is higher than the upper {} -> {}", lower, upper);
    }
    let range = upper - lower + 1;
    println!("The bounds are {} -> {} which is a range of {}", lower, upper, range);
    let ld = time * lower - lower.pow(2);
    println!("The lower distance is {} = ({} * {}) - {}^2 which is better than {}", ld, time, lower, lower, distance);
    let ud = time * upper - upper.pow(2);
    println!("The upper distance is {} = ({} * {}) - {}^2 which is better than {}", ud, time, upper, upper, distance);
    range
}
