import preprocess
import llm_query
import slice
import get_results
import argparse
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='DualLM: A tool for processing commits and LLM queries')
    parser.add_argument('--commits', type=str, nargs='+', default=[], help='List of commits to be processed')
    parser.add_argument('--name', type=str, required=True, help='Name of the evaluation dataset')
    parser.add_argument('--out-file1', type=str, default='out1.txt', help='Output file for the first LLM step')
    parser.add_argument('--out-file2', type=str, default='out2.txt', help='Output file for the second LLM step')
    parser.add_argument('--repo-dir', type=str, required=True, help='Path to the repository directory')
    parser.add_argument('--summary-file', type=str, required=True, help='Path to the summary file')
    parser.add_argument('--data-dir', type=str, required=True, help='Path to the data directory')
    parser.add_argument('--step1-out-file', type=str, default='data/results/step1_res.txt', help='Output file for step 1 results')
    parser.add_argument('--step2-out-file', type=str, default='data/results/step2_res.txt', help='Output file for step 2 results')

    # Parse arguments
    args = parser.parse_args()

    # Query the LLM with the commits
    #llm_query.llm_query(args.commits, args.out_file1, args.out_file2)
   
    
    
    # Get the results from the LLM query
    not_reliable, out_str = get_results.parse_llm_results(args.out_file2)
    
    print("*not_reliable*")
    print(not_reliable)
    print("out_str")
    print(out_str)
    
    # Slice the commits based on the LLM results
    slice.given_slice(not_reliable, args.name, args.repo_dir)
    #slice.given_slice(["42bf546c1fe3"], args.name, args.repo_dir)
    
    
    # Get the summaries from the LLM
    llm_query.get_summaries(not_reliable, args.summary_file)
    
    # Preprocess the data for evaluation
    #preprocess.build_eval_data_for_random_given(args.name, not_reliable, args.data_dir)
    
    # Parse the results from the slicelm
    #out_str = get_results.parse_sliceLM_results(not_reliable, args.step1_out_file, args.step2_out_file)
    #print(out_str)

if __name__ == "__main__":
    main()
    
    