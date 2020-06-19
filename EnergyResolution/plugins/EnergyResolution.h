#ifndef ENERGYRESOLUTION_H
#define ENERGYRESOLUTION_H
#ifndef ROOT_RtypesCore
#include <RtypesCore.h>
#endif

#include <map>
#include <string>
#include <vector>
#include <TH1.h>

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/HGCRecHit/interface/HGCRecHitCollections.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/CaloRecHit/interface/CaloCluster.h"
#include "Geometry/HGCalGeometry/interface/HGCalGeometry.h"
// #include "SimDataFormats/CaloAnalysis/interface/CaloParticle.h"



class EnergyResolution : public edm::EDAnalyzer
{

  public:
    explicit EnergyResolution ( const edm::ParameterSet& );
    ~EnergyResolution ();
    
  private:
    virtual void beginJob () override;
    virtual void analyze ( const edm::Event&, const edm::EventSetup& );
    virtual void endJob () override;
  
    std::vector<math::XYZTLorentzVectorF> getTruthP4 ( const reco::GenParticleCollection & );
    
    void fillHist_HGCalRecHitsEnergy_coneR ( const math::XYZTLorentzVectorF &, const HGCRecHitCollection &, const HGCalGeometry * );
    void fillHist_CaloClustersEnergy_coneR ( const math::XYZTLorentzVectorF &, const std::vector<reco::CaloCluster> &);

    // Container
    std::map <std::string, TH1F*> histContainer_; // map of histograms

    // ------ Data members -------
    // Tokens
    edm::EDGetTokenT<HGCRecHitCollection> token_HGCRecHits_;
    edm::EDGetTokenT<std::vector<reco::CaloCluster>> token_HGCalLayerClustersHFNose_;
    edm::EDGetTokenT<reco::GenParticleCollection> token_GenParticle_;
    // edm::EDGetTokenT<std::vector<CaloParticle>> token_CaloParticle_MergedCaloTruth_;
    
    // Input Tags
    edm::InputTag tag_HGCHFNoseRecHits_;
    edm::InputTag tag_HGCalLayerClustersHFNose_;
    edm::InputTag tag_GenParticle_;
    // edm::InputTag tag_CaloParticle_MergedCaloTruth_;
    
    // Others
    Int_t   select_PID_;
    Float_t select_EtaLow_;
    Float_t select_EtaHigh_;
    Float_t select_coneR_;
};

#endif
