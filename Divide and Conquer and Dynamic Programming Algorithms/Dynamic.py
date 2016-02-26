import timeit


def maxSumDynamic(array):
	maxA = array[0]
	sumA = [0] * len(array)
	sumA[0] = array[0]
	maxInd = 0

	for i in range(len(array)):
		sumA[i] = max(sumA[i-1]+ array[i], 0)
		#maxA = max(maxA, sumA[i])
		if maxA < sumA[i]:
			maxA = sumA[i]
			maxInd = i

	return [maxA, 0, maxInd]

if __name__ == '__main__':
  fout = open('nsagar3_output_dp_10000.txt', "a")	
  with open('10000.txt') as f:
    	n, k = [int(x) for x in f.readline().split(',')]
    	array = [[float(x) for x in line.split(',')] for line in f]
  for a in array:
    start = timeit.default_timer()
    max_sum = maxSumDynamic(a)
    max_sum[2] += 1
    temp_sum = 0
    temp_ind = max_sum[2]-1
    minInd = None
    while temp_sum < max_sum[0] and temp_ind >= 0:
    	temp_sum += a[temp_ind]
    	minInd = temp_ind
    	temp_ind -= 1
    stop = timeit.default_timer()
    max_sum[1] = minInd + 1
    fout.write(','.join(map(str, max_sum)) +" ,"+str((stop-start)*1000)+"\n")
    #print(str(max_sum)+" "+str((stop-start)*1000))
    print(str((stop-start)*1000))
  fout.close()