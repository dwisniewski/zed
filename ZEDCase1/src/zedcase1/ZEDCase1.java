/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package zedcase1;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;

/**
 *
 * @author dawid
 */
public class ZEDCase1 {
    static int[] gainRatioRank0 = new int[] {21,22,87,17,53,73,96,100,65,6,7,1,2,90,81,93,89,16,119,121,61,83,55,62,71,97,104,108,45,116,26,23,98,70,57,49,51,66,35,80,56,28,59,18,95,50,39,105,102,10,68,88,117,64,74,120,85,101,34,94,118,103,52,67,3,4,31,9,8,54,15,79,91,29,76,109,86,63,111,42,60,113,72,78,43,112,36,106,38,114,30,77,40,5,58,107,84,110,48,99,44,115,122,37,24,27,92,33,125,75,47,41,124,46,19,14,20,69,82,123,25,13,11,32,12};
    public static double[] FScores = new double[300];
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*Instances inst = loadData("/home/dawid/Pobrane/train000.arff");
        Instances test = loadData("/home/dawid/Pobrane/test000.arff");
        int attributes = inst.numAttributes();
        
        double bestF = 0;
        for(int i=0; i<attributes; i++) {
            System.out.print(i + "/" + attributes+",");
            inst = loadData("/home/dawid/Pobrane/train000.arff");
            test = loadData("/home/dawid/Pobrane/test000.arff");
            inst.deleteAttributeAt(i);
            test.deleteAttributeAt(i);
            double res = optimizeAttributes(inst, test);
            if(res > bestF) {
                bestF = res;
            }
        }
        System.out.println(bestF);*/
        ExecutorService executor = Executors.newFixedThreadPool(8);
        //Instances inst = loadData("/home/dawid/Pobrane/train000.arff");
        //Instances test = loadData("/home/dawid/Pobrane/test000.arff");
        Instances inst = loadData("D:\\projects\\zed-case\\zed\\Data\\train000.arff");
        Instances test = loadData("D:\\projects\\zed-case\\zed\\Data\\test000.arff");
        
        int attributes = inst.numAttributes();
        
        /*for (int i = 0; i < attributes-1; i++) {
            Runnable worker = new Worker();
            ((Worker)worker).setArg(i);
            executor.execute(worker);
        }
        executor.shutdown();
        while (!executor.isTerminated()) {
        }
        
        double bestF = 0.0;
        for(int i=0; i<FScores.length; i++) {
            if(FScores[i] > bestF) {
                bestF = FScores[i];
            }
        }
        System.out.println(bestF);
    
    */
        System.out.println(optimizeAttributes(inst, test));
    }
    
    public static Instances loadData(String filepath) {
        BufferedReader breader = null;
        try {
            breader = new BufferedReader(new FileReader(filepath));
            Instances instances = new Instances(breader);
            instances.setClassIndex(instances.numAttributes()-1);
            breader.close();
            return instances;
        }
        catch(Exception e) {
            e.printStackTrace();
            return null;
        }
    }
    
    public static double optimizeAttributes(Instances inst, Instances test) {
        Classifier c = new RandomForest();
        try {
            c.buildClassifier(inst);
            Evaluation e = new Evaluation(inst);
            e.evaluateModel(c, test);
            double totalPrec = 0.0, totalRecall = 0.0;
            for(int i=0; i<8; i++) {
                //System.out.println(e.precision(i) + " " + e.recall(i));
                totalPrec += e.precision(i);
                totalRecall += e.recall(i);
            }
            double P = totalPrec/8;
            double R = totalRecall/8;
            return 2.0*P*R/(P+R);
        }
        catch(Exception e) {
            e.printStackTrace();
            return 0;
        }
            
    }
    
}
