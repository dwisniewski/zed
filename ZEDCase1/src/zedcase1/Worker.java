/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package zedcase1;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.logging.Level;
import java.util.logging.Logger;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import static zedcase1.ZEDCase1.loadData;
import static zedcase1.ZEDCase1.optimizeAttributes;

/**
 *
 * @author dawid
 */
public class Worker implements Runnable {
    
    private int arg;
    
    public void setArg(int argVal) {
        arg = argVal;
    }
    
    @Override
    public void run() {
        System.out.println(arg);
        Instances inst = loadData("/home/dawid/Pobrane/train000.arff");
        Instances test = loadData("/home/dawid/Pobrane/test000.arff");
        inst.deleteAttributeAt(arg);
        test.deleteAttributeAt(arg);
        double res = optimizeAttributes(inst, test);
        ZEDCase1.FScores[arg] = res;
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
