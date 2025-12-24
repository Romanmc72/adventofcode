enum RuntimeError : Error {
  case parseError(description: String)
  case illegalState(description: String)
}
