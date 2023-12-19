use std::cmp;
mod common;
mod range;
mod transformers;


/// Description
/// -----------
/// Takes the mappings and the seeds and parses out the seed list and the mappings
/// list into transformers then applies the transformations to the seed list over
/// and over for each transformer set.
fn main() {
    let (lines, part) = common::get_file_and_part();
    if part == 1 {
        let mut first_line = true;
        let mut next_are_sub_transformers = false;
        let mut seeds: Vec<u64> = vec![];
        let mut transformer = transformers::Transformer::new();
        for line in lines {
            if first_line {
                seeds = extract_seeds(line);
                first_line = false;
                println!("Initial Seeds: {:?}", seeds);
            } else if line == "" {
                transformer.transform_seeds(&mut seeds);
                transformer = transformers::Transformer::new();
                next_are_sub_transformers = true;
            } else if next_are_sub_transformers {
                next_are_sub_transformers = false;
                println!("{}", line);
            } else {
                let sub_transformer = transformers::SubTransformer::from_text_line(&line);
                transformer.add_sub_transformer(sub_transformer);
            }
        }
        transformer.transform_seeds(&mut seeds);
        println!("Final Seeds: {:?}", seeds);
        let mut min_seed: u64 = 999999999999999;
        for seed in seeds.iter() {
            min_seed = cmp::min(*seed, min_seed);
        }
        println!("Min Seed={}", min_seed);
    } else if part == 2 {
        let mut seed_ranges: Vec<range::DivisibleRange> = vec![];
        let mut first_line = true;
        let mut next_are_sub_transformers = false;
        let mut transformer = transformers::Transformer::new();
        for line in lines {
            if first_line {
                seed_ranges = extract_seeds_part_2(line);
                first_line = false;
                println!("Initial Seeds: {:?}", seed_ranges);
            } else if line == "" {
                // transform_seeds(&mut transformer, &mut seeds);
                transformer = transformers::Transformer::new();
                next_are_sub_transformers = true;
            } else if next_are_sub_transformers {
                next_are_sub_transformers = false;
                println!("{}", line);
            } else {
                let sub_transformer = transformers::SubTransformer::from_text_line(&line);
                transformer.add_sub_transformer(sub_transformer);
            }
        }
    }
}


/// Description
/// -----------
/// Extracts the seeds from the original line 1 of the text input.
///
/// Params
/// ------
/// :line: String
/// The line of text to get the seeds from.
///
/// Return
/// ------
/// Vec<u64>
/// The vector of numbers representing the seeds.
fn extract_seeds(line: String) -> Vec<u64> {
    let split_line: Vec<&str> = line.split(": ").collect();
    let second_half = split_line.get(1).unwrap();
    common::split_text_to_numbers(second_half)
}


/// Description
/// -----------
/// Extract the seeds as numeric ranges instead of individual numbers.
///
/// Params
/// ------
/// :line: String
/// The line of text containing the seeds to extract.
///
/// Return
/// ------
/// Vec<DivisibleRange>
/// The vector of divisible ranges found inside the text.
fn extract_seeds_part_2(line: String) -> Vec<range::DivisibleRange> {
    let mut seed_ranges = vec![];
    let og_seeds = extract_seeds(line);
    let end_of_index = og_seeds.len() / 2;
    for index in 0..end_of_index {
        let seed_start_index = index * 2;
        let seed_range_index = seed_start_index + 1;
        let seed_start = og_seeds.get(seed_start_index).unwrap();
        let seed_range = og_seeds.get(seed_range_index).unwrap();
        let div_range = range::DivisibleRange::new(*seed_start, seed_start + seed_range - 1);
        seed_ranges.push(div_range);
    }
    seed_ranges
}



/// Description
/// -----------
/// Transforms the seed ranges using the transformer specified.
fn transform_seeds_part_2(transformer: &mut transformers::Transformer, seed_ranges: &mut Vec<range::DivisibleRange>) {}
