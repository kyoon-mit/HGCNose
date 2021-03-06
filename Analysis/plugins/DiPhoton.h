#ifndef DIPHOTON_H
#define DIPHOTON_H

// Standard libraries
#include <map>
#include <string>
#include <vector>
#include <TH1.h>

// ROOT Rtypes
#include <RtypesCore.h>

// EDAnalyzer base class
#include "FWCore/Framework/interface/EDAnalyzer.h"

// Other CMSSW includes that are needed in this header
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/HGCRecHit/interface/HGCRecHitCollections.h"

// Forward declarations
class TH1F;
// class TH2F;

class CaloParticle;

class HGCalGeometry;

namespace reco
{
    class GenParticle;
    typedef std::vector<GenParticle> GenParticleCollection;
    class CaloCluster;
}


// DiPhoton class definition
class DiPhoton : public edm::EDAnalyzer
{

  public:
    explicit DiPhoton ( const edm::ParameterSet& );
    ~DiPhoton ();
    
  private:
    virtual void beginJob () override;
    virtual void analyze ( const edm::Event&, const edm::EventSetup& );
    virtual void endJob () override;
  
    std::vector<math::XYZTLorentzVectorF> getGenTruthP4 ( const reco::GenParticleCollection & );
    std::vector<math::XYZTLorentzVectorF> getCaloTruthP4 ( const std::vector<CaloParticle> & );
    
    // For testing
    void fillHist_ShowerShapeVariables ( const std::vector<reco::CaloCluster> &, const HGCRecHitCollection & );
    
    //getClusters ();
    
    std::vector<math::XYZTLorentzVectorF> getPhotonJets ( );

    // Container
    std::map <std::string, TH1F*> TH1_Container_; // map of histograms

    // ------ Data members -------
    // Tokens
    edm::EDGetTokenT<std::vector<CaloParticle>> token_CaloParticle_MergedCaloTruth_;
    edm::EDGetTokenT<reco::GenParticleCollection> token_GenParticle_;
    edm::EDGetTokenT<HGCRecHitCollection> token_HGCHFNoseRecHits_;
    edm::EDGetTokenT<std::vector<reco::CaloCluster>> token_HGCalLayerClustersHFNose_;
    
    // Input Tags
    edm::InputTag tag_CaloParticle_MergedCaloTruth_;
    edm::InputTag tag_GenParticle_;
    edm::InputTag tag_HGCHFNoseRecHits_;
    edm::InputTag tag_HGCalLayerClustersHFNose_;
    
    // Others
    Int_t   select_PID_;
    Float_t select_EtaLow_;
    Float_t select_EtaHigh_;
    Float_t select_coneR_;
};

#endif
