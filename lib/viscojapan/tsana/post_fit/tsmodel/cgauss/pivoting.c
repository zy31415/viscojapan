#include<stdio.h>
#include<math.h>


void printm(double *arr, int m, int n){
	double *p = arr;
	int i, j;
	for(i = 0; i < m; i++){
		for(j = 0; j < n; j++){
			printf("%10.1f",*p);
			p++;
		}
		printf("\n");
	}
}

void sprintm(char *buff, double *arr, int m, int n){
	double *p = arr;
	int i, j;
	for(i = 0; i < m; i++){
		for(j = 0; j < n; j++){
			sprintf(buff, "%10.1f",*p);
			p++;
		}
		sprintf(buff, "\n");
	}
}

int swap_rows(double *arr, int nrow, int ncol, int m, int n){
	if (n!=m){
		int ni;
		double tp;
		double *p = arr + ncol * m;
		double *q = arr + ncol * n;
		for(ni = 0; ni < ncol; ni++){
			tp = *p; *p = *q; *q = tp;
			p++;
			q++;
		}
	}
	return 0;
}

int cpivoting(double *A, int nrow_A, int ncol_A, double *B, int nrow_B, int ncol_B, int csz){
	int m,mi,n;
	double *p, max;
	nrow_A = nrow_A - csz;
	for(m = 0; m < nrow_A; m++){

#ifdef DEBUG
		printf("m = %d\n",m);
		printm(A,nrow_A,ncol_A);
		printf("\n");
#endif
		
		p = A + m*(ncol_A + 1);
		max = fabs(*p);
		n = m;
		for(mi = m + 1; mi < nrow_A; mi++){
			p += ncol_A;
			if (fabs(*p) > max){
				max = fabs(*p);
				n = mi;
			}
		}
		if (n != m){
			swap_rows(A, nrow_A, ncol_A, m, n);
			swap_rows(B, nrow_B, ncol_B, m, n);
		}
	}
	return 0;
}

