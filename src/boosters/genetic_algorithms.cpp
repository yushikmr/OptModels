#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

class Individual{
    public:
        std::vector<double> variables;
        int num_objects;
        std::vector<double> objects;
        int rank;
        Individual(std::vector<double> variables0, int num_objects0){
            variables = variables0; 
            num_objects = num_objects0;
        };
        Individual update_variavles(std::vector<double> new_vatiables){
            return Individual(new_vatiables, num_objects);
        }
};

class Population{
    public:
        std::vector<Individual> members;
        int num_members;
        Population(std::vector<Individual> members0 = {}){
            members = members0;
            num_members = members.size();
        }
        std::vector<std::vector<double> > extract_objects(){
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
};

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
                nc += NSGA::sharingfunction(ind, population[i], shigma);
            }
            return nc;
        }
        Population select(Population population, int num){
            Population sorted_population = NSGA::nondominatedsort(population);
            Population next_population(std::vector<Individual> {});
            int rank = 1;
            while (next_population.num_members <= num)
            {
                /* code */
                std::vector<Individual> rank_mb = population.rank_memebers(rank);
                if (next_population.num_members + rank_mb.size() <= num)
                {
                    /* code */
                    next_population = next_population.add_members(rank_mb);
                }
                else{
                    int remainder = num - next_population.num_members;
                    // Calculate niche count
                    std::vector<double> nc_s{};
                    for(int8_t i=0; i < rank_mb.size(); i++){
                        nc_s.push_back(NSGA::niche_count(rank_mb[i], next_population, shigma));
                    }
                    // sorting niche count
                    std::sort(nc_s.begin(), nc_s.end() , std::greater<double>());
                    double thred_nc = nc_s[remainder];
                    // select add members by niche_count
                    std::vector<Individual> nc_memb{};
                    for(int8_t i=0; i < rank_mb.size(); i++){
                        if (nc_s[i] > thred_nc){
                            nc_memb.push_back(rank_mb[i]);
                            if (nc_memb.size() >= remainder){
                                break;
                            }
                        }
                    }
                    next_population = next_population.add_members(nc_memb);    
                }
                
                rank += 1;
            }  

            return next_population;
        }
        
};





int main(){
    Individual ind1({1,1,1}, 2);
}