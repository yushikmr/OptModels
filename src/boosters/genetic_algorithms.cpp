#include <vector>
#include <cmath>
#include <algorithm>
#include <limits>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

class Individual{
    public:
        std::vector<double> variables;
        int num_objects;
        std::vector<double> objects;
        int rank;
        double nc;

        Individual(std::vector<double> variables0, 
                   int num_objects0
                   ){
            variables = variables0; 
            num_objects = num_objects0;
            rank=0;
        };
        // constructor for allocate objects
        Individual(std::vector<double> variables0, 
                   int num_objects0,
                   std::vector<double> objects0){
            variables = variables0; 
            num_objects = num_objects0;
            objects = objects0;
            rank=0;
                   };
        Individual(std::vector<double> variables0, 
                   int num_objects0,
                   std::vector<double> objects0,
                   int rank0,
                   double nc0){
            variables = variables0; 
            num_objects = num_objects0;
            objects = objects0;
            rank = rank0;
            nc = nc0;
                   };

        Individual update_variavles(std::vector<double> new_vatiables){
            return Individual(new_vatiables, num_objects);
        };
        Individual allocate_objects(std::vector<double> new_objects){
            return Individual(variables, num_objects, new_objects);
        }
        Individual allocate_rank(int new_rank){
            return Individual(variables, num_objects, objects, new_rank, nc);
        }
        Individual allocate_nc(double new_nc) const {
            return Individual(variables, num_objects, objects, rank, new_nc);
        }

};


bool operator> (const Individual &left, const Individual &right){
    if (left.rank != right.rank)
    {
        return left.rank < right.rank;
    }
    else{
        return left.nc > right.nc;
    }
}

bool operator>= (const Individual &left, const Individual &right){
    if (left.rank != right.rank)
    {
        return left.rank <= right.rank;
    }
    else{
        return left.nc >= right.nc;
    }
}

class Population{
    public:
        std::vector<Individual> members;
        int num_members;
        Population(std::vector<Individual> members0 = {}){
            members = members0;
            num_members = members.size();
        }
        std::vector<std::vector<double> > extract_objects() const {
            std::vector<std::vector<double> > objects{};
            for (int8_t i=0; i < num_members; i++){
                objects.push_back(members[i].objects);
            }
            return objects;
        }
        Population add_members(std::vector<Individual> new_members){
            std::vector<Individual> all_members ;
            members.insert(members.end(), new_members.begin(), new_members.end());
            return Population(all_members);
        }
        std::vector<Individual> rank_memebers(int rank){
            std::vector<Individual> push_members = {};
            for(int8_t i=0; i < num_members; i++){
                if (members[i].rank == rank){
                    push_members.push_back(members[i]);
                }
            }
            return push_members;
        }
        static bool compare_inds(const Individual &left, const Individual &right){
            if (left.rank != right.rank)
            {
                return left.rank < right.rank;
            }
            else{
                return left.nc > right.nc;
            }
        }
        Population sorted(){
            std::vector<Individual>  sorted_members = members;
            std::sort(sorted_members.begin(), sorted_members.end(), Population::compare_inds);
            return Population(sorted_members);
        }

};

Population operator+(const Population &left, const Population &right){
    std::vector<Individual> new_members;
    new_members.insert(new_members.end(), left.members.begin(), left.members.end());
    new_members.insert(new_members.end(), right.members.begin(), right.members.end());
    Population new_population(new_members);
    return new_population;
}

class NSGA{
    public:
        int generation;
        int numvariables;
        int numobjects;
        double low, up, shigma;

        NSGA(int generation0, 
             int numvariables0, 
             int numobjects0, 
             double low0, 
             double up0, 
             double shigma0){
                 generation = generation0; 
                 numvariables = numvariables0; 
                 numobjects = numobjects0;
                 low = low0;
                 up = up0;
                 shigma = shigma0;
             }
        Population evolution(Population population);
        Population evaluation(Population population);
        Population nondominatedsort(Population poplation);

        Population niche_count(const Population &population){
            int num = population.num_members;
            std::vector<Individual> new_members;
            std::vector<std::vector<double> > pop_objs = population.extract_objects();
            for (int i=0;i<num; i++){
                double nc = NSGA::_niche_count(population.members[i].objects, pop_objs, shigma);
                Individual newind = population.members[i].allocate_nc(nc);
                new_members.push_back(newind);
            }
            return Population(new_members);
        }
    protected:

        double _sharingfunction(const std::vector<double> & obj1, 
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

        double _niche_count(const std::vector<double> & objs, 
                        const std::vector<std::vector<double> > & pop_objs, 
                        const double & shigma){
            double nc=0, N;
            N = pop_objs.size();
            for (size_t i = 0; i < N; i++)
            {
                /* code */
                nc += NSGA::_sharingfunction(objs, pop_objs[i], shigma);
            }
            return nc;
        }
        
};


double sample(double a, double b){
    return a + b;
}


namespace py = pybind11;
PYBIND11_MODULE(genetic_algorithms, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    py::class_<Individual>(m, "Individual")
              .def(py::init<std::vector<double>, int >())
              .def(py::self > py::self)
              .def(py::self >= py::self)
              .def_readwrite("variables", &Individual::variables)
              .def_readwrite("objects", &Individual::objects)
              .def_readwrite("num_objects", &Individual::num_objects)
              .def_readwrite("rank", &Individual::rank)
              .def_readwrite("nc", &Individual::nc)
              .def("update_variables", &Individual::update_variavles)
              .def("allocate_objects", &Individual::allocate_objects, "allocate objects to individual")
              .def("allocate_nc", &Individual::allocate_nc, "allocate niche count to individual")
              .def("allocate_rank", &Individual::allocate_rank, "allocate rank to individual");
    py::class_<Population>(m, "Population")
              .def(py::init<const std::vector<Individual> &>())
              .def_readwrite("members", &Population::members)
              .def(py::self + py::self)
              .def("sorted", &Population::sorted);
    m.def("add", &sample, "sample function", py::arg("a")=0, py::arg("b")=0);
    py::class_<NSGA>(m, "NSGA")
              .def(py::init<int, int, int, double, double, double>())
              .def_readwrite("numvariables", &NSGA::numvariables)
              .def_readwrite("numobjects", &NSGA::numobjects)
              .def_readwrite("low", &NSGA::low)
              .def_readwrite("up", &NSGA::up)
              .def_readwrite("shigma", &NSGA::shigma)
              .def("niche_count", &NSGA::niche_count);


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
