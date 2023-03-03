"""
Architecture,Benchmark,Instruction Cache Size [B],Data Cache Size [B],CPI
X86,crc,128,128,23.96873798
X86,crc,128,256,21.96031175
X86,crc,128,512,15.79506549
X86,crc,128,1024,13.14101658
X86,crc,128,2048,10.43260317
X86,crc,128,4096,8.985780024
X86,crc,128,8192,8.924989993
X86,crc,128,16384,8.866611478
X86,crc,128,32768,8.862300337
X86,crc,128,65536,8.862266454
X86,crc,128,131072,8.862258427
X86,crc,128,262144,8.862258427
X86,crc,256,128,18.52948372
X86,crc,256,256,16.48157796
X86,crc,256,512,10.39809423
X86,crc,256,1024,7.791961358
X86,crc,256,2048,5.120722254
X86,crc,256,4096,3.693386504
X86,crc,256,8192,3.638900286
X86,crc,256,16384,3.585534806
X86,crc,256,32768,3.581717937
X86,crc,256,65536,3.581643291
X86,crc,256,131072,3.581633491
X86,crc,256,262144,3.581633491
X86,crc,512,128,18.54728141
X86,crc,512,256,16.48151906
X86,crc,512,512,10.39722287
X86,crc,512,1024,7.791491013
X86,crc,512,2048,5.12069447
X86,crc,512,4096,3.695019028
X86,crc,512,8192,3.638230658
X86,crc,512,16384,3.585027659
X86,crc,512,32768,3.581174874
X86,crc,512,65536,3.581152512
X86,crc,512,131072,3.581141982
X86,crc,512,262144,3.581141982
X86,crc,1024,128,18.53205152
X86,crc,1024,256,16.47964059
X86,crc,1024,512,10.39587022
"""

if __name__ == "__main__":
    import argparse, csv
    from os import path, makedirs
    import matplotlib.pyplot as plt
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_file",
        action="store",
        default="results.csv",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        action="store",
        default="out/plots",
        type=str,
        nargs=1,
    )
    
    args = parser.parse_args()
    
    if not path.exists(args.output_directory):
        makedirs(args.output_directory)
    
    with open(args.input_file, "r") as input_file:
        reader = csv.reader(input_file)
        results = list(reader)
    
    # print cpi against dcache size for each icache size for each benchmark for each architecture
    for architecture in set(row[0] for row in results[1:]):
        for benchmark in set(row[1] for row in results[1:]):
            fig, ax = plt.subplots()
            unsorted_set = set(row[2] for row in results[1:])
            sorted_set = sorted(unsorted_set, key=lambda x: int(x))
            # print(sorted_set)
            for icache_size in sorted_set:
                print(icache_size)
                x = []
                y = []
                for row in results[1:]:
                    if row[0] == architecture and row[1] == benchmark and row[2] == icache_size:
                        print(row[3])
                        x.append(int(row[3]))
                        y.append(float(row[4]))

                if int(icache_size) > 512:
                    legend_icache = str(int(int(icache_size)/1024)) + "KB"
                else:
                    legend_icache = str(icache_size) + "B"


                ax.plot(x, y, label=f"{legend_icache}")
            plt.xscale("log", base=2)
            
            ax.set_xlabel(results[0][3])
            ax.set_ylabel(results[0][4])
            ax.set_title(f"{architecture} {benchmark} Cache Size vs CPI1")
            ax.legend()
            fig.savefig(f"{args.output_directory}/{architecture}_{benchmark}.png")