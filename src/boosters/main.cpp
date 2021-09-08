#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)


double sharingfunction(const std::vector<double> & obj1, 
                       const std::vector<double> & obj2, 
                       const double & shigma){
    int l1, l2;
    double d2=0, d=0;
    l1 = obj1.size();
    l2 = obj2.size();
    if (l1 != l2){
        throw "the size of obj1 is different from that of obj2.";
    }
    for (size_t i = 0; i < l1; i++)
    {
        double x1 = obj1[i];
        double x2 = obj2[i];
        double s = std::pow((x1 - x2), 2);
        d2 += s;
    }
    d = std::pow(d2, 0.5);
    if (d < shigma){
        return 1 - (d / shigma);
    }
    else{
        return 0;
    }
}

double niche_count(const std::vector<double> & ind, 
                   const std::vector<std::vector<double> > & population, 
                   const double & shigma){
    double nc=0, N;
    N = population.size();
    for (size_t i = 0; i < N; i++)
    {
        /* code */
        nc += sharingfunction(ind, population[i], shigma);
    }
    return nc;
    
}



bool is_dominated(std::vector<double> a, std::vector<double> b){
    int i, na, nb, dnm;
    na= a.size();
    nb = b.size();
    if (na != nb){
        throw 0;
    }
    dnm = 0;
    for (i=0;i<na;i++) {
        if (a[i] < b[i]){
            dnm+=1;
        }
    }
    if (dnm == na){
        return  true;
    }
    else{
        return false;
    }
}

int dominated_num(std::vector<double> const & ind, std::vector<std::vector<double> > const  & population){
    int n, N, dnm;
    n = ind.size();
    N = population.size();
    dnm = 0;
    for (int i = 0; i < N; ++i) {
        std::vector<double> const & another = population[i];
        if (is_dominated(ind, another)){ dnm +=1;}
    }
    return dnm;
}



namespace py = pybind11;

PYBIND11_MODULE(genetic_functions, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("is_dominated", &is_dominated, "is dominated");
    m.def("dominated_num", &dominated_num, "count the num of dominated individuals");
    m.def("sharingfunction", &sharingfunction, "sharing function");
    m.def("niche_count", &niche_count, "niche count");


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
