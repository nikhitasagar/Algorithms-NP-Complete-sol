import sys
import timeit

def cross_sum(array, start, middle, end):

  left_sum = float('-inf')
  sum_ = 0
  for i in range(middle, start-1, -1):
    sum_ += array[i]
    if sum_ > left_sum:
    	left_sum = sum_
    	max_left = i

  right_sum = float('-inf')
  sum_ = 0
  for i in range(middle + 1, end+1):
    sum_ += array[i]
    if sum_ > right_sum:
    	right_sum = sum_
    	max_right = i

  return [left_sum + right_sum, max_left, max_right]


def div_conquer(array, start, end):
  if start == end:
    return [array[start], start, end]
  else:
    middle = int((start + end) / 2)
    L = div_conquer(array, start, middle)
    R = div_conquer(array,middle+1, end)
    C = cross_sum(array, start, middle, end)
    if L[0] == max(L[0], R[0], C[0]):
    	return L
    elif R[0] == max(L[0], R[0], C[0]):
    	return R
    elif C[0] == max(L[0], R[0], C[0]):
    	return C    
    #return max(div_conquer(array, start , middle), 
               #div_conquer(array, middle + 1, end),
               #cross_sum(array, start, middle, end))

def main():
	fout = open('nsagar3_output_dc_10000.txt', "a")
	with open('10000.txt') as f:
		n, k = [int(x) for x in f.readline().split(',')]
		array = [[float(x) for x in line.split(',')] for line in f]
	for a in array:
		start = timeit.default_timer()
		max_sum = div_conquer(a,0,n-1)
		max_sum[1]+= 1
		max_sum[2]+= 1
		stop = timeit.default_timer()
		fout.write(','.join(map(str, max_sum)) +" ,"+str((stop-start)*1000)+"\n")
		#print(str(max_sum)+" "+str((stop-start)*1000))
		print(str((stop-start)*1000))
	fout.close()
if __name__ == '__main__':
	main()
