/// Description
/// -----------
/// A stand in for a giant range of numbers which can be divided into several
/// smaller ranges of numbers.
#[derive(Debug, Clone)]
pub struct DivisibleRange {
    pub bottom: u64,
    pub top: u64
}

impl DivisibleRange {
    /// Description
    /// -----------
    /// Instantiates a divisible range given the 2 numbers for the range.
    ///
    /// Params
    /// ------
    /// :bottom: u64
    /// The lowest number in the range.
    ///
    /// :top: u64
    /// The highest number in the range.
    ///
    /// Return
    /// ------
    /// A new divisible range.
    pub fn new(bottom: u64, top: u64) -> DivisibleRange {
        DivisibleRange { bottom, top }
    }

    /// Description
    /// -----------
    /// Divides the divisible range at the divide at point or just returns
    /// the range that was input in a vector by itself.
    ///
    /// Params
    /// ------
    /// :divide_at: u64
    /// A number ideally within the range that will be used to divide the range.
    ///
    /// Return
    /// ------
    /// Vec<DivisibleRange>
    /// A vector of one or two divisible ranges that have been divided on the
    /// divide at number. The divide at number will be kept in the lower of
    /// the 2 ranges and not appear in the upper range.
    pub fn divide_at(&self, divide_at: u64) -> Vec<DivisibleRange> {
        if self.is_in_range(divide_at) {
            if self.top == self.bottom {
                return vec![self.clone(), self.clone()];
            } else {
                return vec![
                    DivisibleRange {bottom: self.bottom, top: divide_at},
                    DivisibleRange {bottom: divide_at + 1, top: self.top},
                ];
            }
        }
        vec![self.clone()]
    }

    /// Description
    /// -----------
    /// Determine whether or not a number lies within the range of a divisible
    /// range.
    ///
    /// Params
    /// ------
    /// :number: u64
    /// The number to test whether or not it is in the range.
    ///
    /// Return
    /// ------
    /// bool
    /// True if the number is within the range.
    /// False if the number is not within the range.
    fn is_in_range(&self, number: u64) -> bool {
        number > self.bottom && number < self.top
    }
}
