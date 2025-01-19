declare module 'flexsearch' {
  class FlexSearch {
    constructor();
    add(id: number, content: string): void;
    search(query: string): Promise<number[]>;
  }

  export default FlexSearch;
}