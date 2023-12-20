/**
 * Need me a way to take the range of source inputs and map them to outputs.
 * Storing and sorting the inner transformers actually makes sense to me so
 * that one can find the transformer that is closes to the input number and
 * check to see if it is actually in range. If it is not in range then we can
 * just return the number and if it is we can return the transformation.
 */
use ranges::DivisibleRange;
use sub_transformer::SubTransformer;


/// Description
/// -----------
/// A transformer with an array of sub transformers inside of it.
pub struct Transformer {
    pub sub_transformers: Vec<SubTransformer>,
}


impl Transformer {
    /// Description
    /// -----------
    /// Instantiates the transformer with nothing inside it.
    pub fn new() -> Transformer {
        Transformer { sub_transformers: vec![] }
    }

    /// Description
    /// -----------
    /// Inserts a sub transformer into the vector of transformers into the
    /// position that it belongs by iterating through the transformers that
    /// exist and adding this transformer after the one that it is bigger than.
    ///
    /// Params
    /// ------
    /// :sub_transformer: SubTransformer
    /// The sub transformer to insert into the list of sub transformers.
    pub fn add_sub_transformer(&mut self, sub_transformer: SubTransformer) {
        let mut insertion_index: usize = 0;
        for sub in self.sub_transformers.iter() {
            if sub_transformer.source > sub.source {
                insertion_index += 1;
            } else {
                break;
            }
        }
        self.sub_transformers.insert(insertion_index, sub_transformer);
    }

    /// Description
    /// -----------
    /// Takes the input number, finds the right transformer for it, and applies
    /// the appropriate transformation to that number using the sub transformer.
    ///
    /// Params
    /// ------
    /// :number: &mut u64
    /// The number to transform in place.
    pub fn transform_number(&mut self, number: &mut u64) {
        for index in 0..self.sub_transformers.len() {
            let sub_transformer = self.sub_transformers.get(index).unwrap();
            let next_sub_transformer = self.sub_transformers.get(index + 1);
            match next_sub_transformer {
                Some(next_sub) => {
                    if *number < next_sub.source && *number >= sub_transformer.source {
                        sub_transformer.transform_number(number);
                        break;
                    }
                },
                None => {
                    sub_transformer.transform_number(number);
                    break;
                },
            }
        }
    }

    /// Description
    /// -----------
    /// Takes the input range, finds the right transformers for it, and applies
    /// the appropriate transformation to that range using the sub transformers.
    ///
    /// Params
    /// ------
    /// :range: &mut DivisibleRange
    /// The range to transform/divide.
    pub fn transform_range(&mut self, range: &mut DivisibleRange) -> Vec<DivisibleRange> {
        let mut transformed_ranges: Vec<DivisibleRange> = vec![];
        let mut leftover_range = true;
        for sub_transformer in self.sub_transformers.iter() {
            let (touched_ranges_maybe, untouched_range_maybe) = sub_transformer.transform_range(range);
            match touched_ranges_maybe {
                Some(touched_ranges) => {
                    for touched_range in touched_ranges.iter() {
                        transformed_ranges.push(touched_range.clone());
                    }
                },
                None => {},
            }
            match untouched_range_maybe {
                Some(untouched_range) => {
                    *range = untouched_range;
                },
                None => {
                    leftover_range = false;
                    break;
                },
            }
        }
        if leftover_range {
            transformed_ranges.push(range.clone());
        }
        transformed_ranges
    }

    /// Description
    /// -----------
    /// Transforms the seeds in place using the transformer.
    ///
    /// Params
    /// ------
    /// :transformer:  &mut Transformer
    /// The transformer used to transform the numbers.
    ///
    /// :seeds: &mut Vec<u64>
    /// The seeds to transform with the transformer.
    pub fn transform_seeds(&mut self, seeds: &mut Vec<u64>) {
        println!("Seeds Pre-Transform: {:?}", seeds);
        for seed in seeds.iter_mut() {
            self.transform_number(seed);
        }
        println!("Transformed Seeds: {:?}", seeds);
    }

    /// Description
    /// -----------
    /// Transforms the seeds in place using the transformer.
    ///
    /// Params
    /// ------
    /// :transformer:  &mut Transformer
    /// The transformer used to transform the numbers.
    ///
    /// :seeds: &mut Vec<u64>
    /// The seeds to transform with the transformer.
    ///
    /// Return
    /// ------
    /// Vec<DivisibleRange>
    /// The vector of transformed seed ranges.
    pub fn transform_seed_ranges(&mut self, seed_ranges: &mut Vec<DivisibleRange>) -> Vec<DivisibleRange> {
        let mut transformed_seed_ranges = vec![];
        for seed_range in seed_ranges.iter_mut() {
            println!("Range Pre-Transform: {:?}", seed_range);
            let transformed_seed_range = self.transform_range(seed_range);
            for range in transformed_seed_range.iter() {
                transformed_seed_ranges.push(range.clone());
            }
            println!("Transformed Range: {:?}", seed_range);
        }
        transformed_seed_ranges
    }
}
