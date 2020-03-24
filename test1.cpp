#include<stdio.h>
#include<string.h>
#include<direct.h>
#include<io.h>
#include <string></span>
using namespace std;
void WC_c(char *Filename);
void WC_w(char *Filename);
void WC_l(char *Filename);
void WC_s(int argc,char *argv[],string Filename);
void do_eve(int argc,char *argv[],char *Filename);
void WC_a(char *Filename);
int main(int argc,char *argv[])
{
    string path_a0;
    char *catalog;
    //printf("argc=%d  %s  \n",argc,argv[0]);
    //printf("argv[argc-1][0]=%c\n",argv[argc-1][0]);
    if(argv[argc-1][0]!='*')
        do_eve(argc,argv,argv[argc-1]);
    else    // -s
        {   getcwd(catalog,100);    //his function in IDE's exe and in DOS's exe are different!
            {   //get right catalog-name in DOS
                path_a0=argv[0];
                path_a0.erase(path_a0.find( '\\',0 ),100 );
                path_a0=catalog+path_a0;
                //printf("path_a0:%s\n",path_a0.c_str( ));
            }
            WC_s(argc ,argv,path_a0 );
            }
    return 0;
}

void WC_c(char *Filename){
    int ch_sum;
    char *ch=Filename;
    FILE *fp;
    fp=fopen( ch,"r") ;
    for(ch_sum=0;feof(fp)==0;ch_sum++)
         fgetc(fp) ;
    printf("ch_sum=%d\n",ch_sum-1); // -1: feof always shows more a char
    //return 0;
}
void WC_w(char *Filename){
    int word_sum=0;
    FILE *fp;
    char c;
    char inchar[256]="_-'";    printf("%s\n",inchar);
    fp=fopen( Filename,"r" );
    while(feof(fp)==0){
            c=fgetc(fp);
        if(c<='z'&&c>='a' || c<='Z'&&c>='A' )
            {
                while(c<='z'&&c>='a' || c<='Z'&&c>='A' || strchr(inchar,c)!=NULL)   //stchr函数...
                c=fgetc(fp);
                word_sum++;
            }
        }printf("word_sum=%d\n",word_sum);
}
void WC_l(char *Filename){
   int line_sum=0;
   FILE *fp;
   fp=fopen( Filename,"r");
   while(feof(fp)==0){
    if(fgetc(fp)=='\n') line_sum++;
   }printf("line_sum=%d\n",line_sum+1);
}
void WC_s(int argc,char *argv[],string Filename){
    struct _finddata_t data;
    long handle;
    int i;
    string fpath = Filename;   //enter folder,for _findfirst()
    fpath = fpath + "\\*";
    //printf("path of exe: %s\n", );
    //printf("fpath:%s\n",fpath.c_str() );
    handle=_findfirst( fpath.c_str() , &data );
    do{
        if(data.attrib & _A_SUBDIR){  //data is a folder
            if(strcmp(data.name,".")!=0 && strcmp(data.name,"..")!=0 ){
                string newpath=Filename;
                newpath=newpath+"\\"+data.name;
                WC_s(argc,argv,newpath);          //DFS
            }
        }
        else
        {
            string newpath2=Filename;
            newpath2=newpath2+"\\"+data.name;
            string match_argv=argv[argc-1];
            match_argv.assign(match_argv,1,100);
            if( newpath2.find(match_argv,0) != -1 )     // if let the return-number >0 ,you'll wrong,why??
                {   printf("%s:\n",newpath2.c_str() );
                    do_eve(argc,argv,const_cast<char *>(newpath2.c_str() ) );//const *char -> *char
                }
        }
    }while(_findnext(handle,&data)==0 );
}
void do_eve(int argc,char *argv[],char *Filename ){
  //exception programming ,not perfect
    int i;
    for(i=1;i<=argc-2;i++){
        if(strcmp(argv[i],"-c")==0 )   WC_c(Filename);
        if(strcmp(argv[i],"-w")==0 )   WC_w(Filename);
        if(strcmp(argv[i],"-l")==0 )   WC_l(Filename);
        if(strcmp(argv[i],"-a")==0 )   WC_a(Filename);
    }
}
void WC_a(char *Filename){
    FILE *fp;
    int i,blankl_sum,codel_sum,commentl_sum,linec_sum;    //linec_sum is amount of valid chars.
    char c;
    fp=fopen(Filename,"r");
    i=blankl_sum=codel_sum=commentl_sum=0;
    for(linec_sum=0; feof(fp)==0 ; ){
        c=fgetc(fp);
        if(c!='\n' && c!='\t' && c!=' '){
                linec_sum++;
                if(c=='"'){
                    c=fgetc(fp);
                    while(c!='"')  {c=fgetc(fp);    //silently deal with
                        linec_sum++;}   //its wrong but ... not all wrong
                }
                else if(c=='/'){
                    c=fgetc(fp);
                    if(c=='*'){
                        for(i=1;1;c=fgetc(fp)){  //silently deal with
                            if(c=='\n') i++;
                            else if(c=='*'){ c=fgetc(fp);
                            if(c=='/') {commentl_sum+=i;    break;}
                            }
                        }
                        while(c!='\n'&& feof(fp)==0) c=fgetc(fp);     //silently deal with '//' and restart a new  line
                        if(linec_sum>1)    codel_sum++;
                        linec_sum=0;
                    }
                    else if(c=='/') {
                            commentl_sum++;
                        while(c!='\n'&& feof(fp)==0) c=fgetc(fp);     //silently deal with '//' and restart a new  line
                        if(linec_sum>1)    codel_sum++;
                        linec_sum=0;
                    }
                }
            }
        else if(linec_sum>1 && c=='\n')     {codel_sum++;   linec_sum=0;}
        else if( c=='\n ')  blankl_sum++;
    }
    printf("codel_sum:%d\ncommentl_sum:%d\nblankl_sum:%d\n",codel_sum,commentl_sum,blankl_sum);
}
